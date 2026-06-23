from django.core.management.base import BaseCommand
from decimal import Decimal
from random import randint, choice, uniform
from accounts.models import User
from ofertas.models import Oferta
from configapp.models import ConfiguracaoIgreja
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Popula o banco com dados de teste'

    def handle(self, *args, **options):
        self.stdout.write('Criando dados de teste...')

        if User.objects.filter(email='admin@igreja.com').exists():
            self.stdout.write('Dados já existem. Pulando...')
            return

        admin = User.objects.create_superuser(
            email='admin@igreja.com',
            nome='Administrador',
            cpf='11111111111',
            password='123456',
            cargo='admin',
            is_dizimista=False,
        )
        admin.profile.theme_primary_color = '#6750A4'
        admin.profile.save()
        self.stdout.write(f'  Admin criado: admin@igreja.com / 123456')

        dizimistas_data = [
            ('João Silva', '12345678901', '(11) 99999-0001'),
            ('Maria Oliveira', '98765432100', '(11) 99999-0002'),
            ('Pedro Santos', '11122233344', '(11) 99999-0003'),
            ('Ana Costa', '55566677788', '(11) 99999-0004'),
            ('Carlos Pereira', '99988877766', '(11) 99999-0005'),
            ('Lucia Souza', '44455566677', '(11) 99999-0006'),
            ('Ricardo Lima', '77788899900', '(11) 99999-0007'),
            ('Fernanda Rocha', '22233344455', '(11) 99999-0008'),
            ('Marcos Paulo', '88877766655', '(11) 99999-0009'),
            ('Juliana Mendes', '66655544433', '(11) 99999-0010'),
            ('Thiago Barbosa', '33344455566', '(11) 99999-0011'),
            ('Patrícia Dias', '12312312312', '(11) 99999-0012'),
            ('Roberto Nunes', '32132132132', '(11) 99999-0013'),
            ('Cristina Alves', '45645645645', '(11) 99999-0014'),
            ('Gustavo Torres', '65465465465', '(11) 99999-0015'),
        ]

        tipos = ['dinheiro', 'cartao', 'pix']
        dizimistas = []

        for nome, cpf, telefone in dizimistas_data:
            email = f'{nome.lower().replace(" ", ".")}@email.com'
            user = User.objects.create_user(
                email=email,
                nome=nome,
                cpf=cpf,
                telefone=telefone,
                password='123456',
                cargo='dizimista',
                is_dizimista=True,
            )
            dizimistas.append(user)
            self.stdout.write(f'  Dizimista criado: {nome} ({email})')

        hoje = date.today()
        ofertas_count = 0

        for dizimista in dizimistas:
            num_ofertas = randint(1, 5)
            for _ in range(num_ofertas):
                dias_atras = randint(0, 180)
                data = hoje - timedelta(days=dias_atras)
                valor = Decimal(str(round(uniform(20, 500), 2)))
                tipo = choice(tipos)

                Oferta.objects.create(
                    valor=valor,
                    dizimista=dizimista,
                    data=data,
                    tipo_pagamento=tipo,
                )
                ofertas_count += 1

        config = ConfiguracaoIgreja.get_instance()
        config.nome = 'Igreja Cristã'
        config.cnpj = '12345678000199'
        config.endereco = 'Rua da Igreja, 123 - Centro'
        config.save()

        self.stdout.write(f'  {ofertas_count} ofertas criadas')
        self.stdout.write('  Configuração da igreja criada')
        self.stdout.write(self.style.SUCCESS('Seed concluído com sucesso!'))
