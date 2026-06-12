from rest_framework import serializers
from .models import ConfiguracaoIgreja, UserProfile


class ConfiguracaoIgrejaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracaoIgreja
        fields = ['nome', 'cnpj', 'endereco']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['theme_primary_color']
