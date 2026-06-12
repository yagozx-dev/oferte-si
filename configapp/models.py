from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class ConfiguracaoIgreja(models.Model):
    nome = models.CharField(max_length=255, default='')
    cnpj = models.CharField(max_length=18, default='', blank=True)
    endereco = models.TextField(default='', blank=True)

    class Meta:
        verbose_name = 'Configuração da Igreja'
        verbose_name_plural = 'Configurações da Igreja'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.nome or 'Configuração da Igreja'


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    theme_primary_color = models.CharField(
        max_length=7,
        default='#6750A4'
    )

    def __str__(self):
        return f'Perfil de {self.user.nome}'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
