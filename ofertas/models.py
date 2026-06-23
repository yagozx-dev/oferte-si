from django.db import models
from django.conf import settings


class Oferta(models.Model):
    TIPO_PAGAMENTO_CHOICES = [
        ('dinheiro', 'Dinheiro'),
        ('cartao', 'Cartão'),
        ('pix', 'PIX'),
    ]

    valor = models.DecimalField(max_digits=10, decimal_places=2)
    dizimista = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ofertas'
    )
    data = models.DateField()
    tipo_pagamento = models.CharField(
        max_length=20,
        choices=TIPO_PAGAMENTO_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Oferta de {self.dizimista.nome} em {self.data}'
