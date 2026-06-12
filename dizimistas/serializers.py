from rest_framework import serializers
from accounts.models import User


class DizimistaListSerializer(serializers.ModelSerializer):
    total_ofertas_mes = serializers.SerializerMethodField()
    ultima_oferta_data = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    total_ofertas_valor = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'nome', 'cpf', 'telefone', 'email', 'total_ofertas_mes',
                  'ultima_oferta_data', 'status', 'total_ofertas_valor']

    def get_total_ofertas_mes(self, obj):
        mes = self.context.get('mes')
        ano = self.context.get('ano')
        if mes and ano:
            return obj.ofertas.filter(data__year=ano, data__month=mes).count()
        from datetime import date
        hoje = date.today()
        return obj.ofertas.filter(data__year=hoje.year, data__month=hoje.month).count()

    def get_ultima_oferta_data(self, obj):
        ultima = obj.ofertas.order_by('-data').first()
        return ultima.data.isoformat() if ultima else None

    def get_status(self, obj):
        total = self.get_total_ofertas_mes(obj)
        return 'ofertou' if total > 0 else 'nao_ofertou'

    def get_total_ofertas_valor(self, obj):
        mes = self.context.get('mes')
        ano = self.context.get('ano')
        if mes and ano:
            ofertas = obj.ofertas.filter(data__year=ano, data__month=mes)
        else:
            from datetime import date
            hoje = date.today()
            ofertas = obj.ofertas.filter(data__year=hoje.year, data__month=hoje.month)
        total = sum(o.valor for o in ofertas)
        return float(total)
