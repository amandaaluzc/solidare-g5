# Generated by Django 5.2 on 2025-05-16 21:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Crianca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('idade', models.IntegerField()),
                ('descricao', models.TextField()),
                ('foto', models.ImageField(blank=True, null=True, upload_to='fotos/')),
            ],
        ),
        migrations.CreateModel(
            name='Padrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefone', models.CharField(max_length=20)),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('metodo_pagamento', models.CharField(choices=[('credit', 'Cartão de crédito'), ('pix', 'PIX'), ('boleto', 'Boleto')], max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='padrinho', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Apadrinhamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_apadrinhamento', models.DateTimeField(auto_now_add=True)),
                ('crianca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apadrinhamento.crianca')),
                ('padrinho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apadrinhamento.padrinho')),
            ],
        ),
    ]
