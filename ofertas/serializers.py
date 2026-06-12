from rest_framework import serializers
from .models import Oferta


class OfertaSerializer(serializers.ModelSerializer):
    dizimista_nome = serializers.CharField(source='dizimista.nome', read_only=True)

    class Meta:
        model = Oferta
        fields = ['id', 'valor', 'dizimista', 'dizimista_nome', 'data', 'tipo_pagamento', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
