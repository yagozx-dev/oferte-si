from rest_framework import viewsets
from .models import Oferta
from .serializers import OfertaSerializer


class OfertaViewSet(viewsets.ModelViewSet):
    queryset = Oferta.objects.all().select_related('dizimista').order_by('-data')
    serializer_class = OfertaSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        dizimista = self.request.query_params.get('dizimista', '')
        data_gte = self.request.query_params.get('data__gte', '')
        data_lte = self.request.query_params.get('data__lte', '')
        tipo = self.request.query_params.get('tipo_pagamento', '')

        if dizimista:
            qs = qs.filter(dizimista_id=dizimista)
        if data_gte:
            qs = qs.filter(data__gte=data_gte)
        if data_lte:
            qs = qs.filter(data__lte=data_lte)
        if tipo:
            qs = qs.filter(tipo_pagamento=tipo)

        return qs
