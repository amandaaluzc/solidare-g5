from django.db import models
from django.contrib.auth.models import User


class Crianca(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    descricao = models.TextField()
    foto = models.ImageField(upload_to="fotos/")

    def __str__(self):
        return self.nome

class Padrinho(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="padrinho")
    telefone = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14, unique=True)
    
    PAGAMENTO_OPCOES = [
        ("credit",  "Cartão de crédito"),
        ("pix",     "PIX"),
        ("boleto",  "Boleto"),
    ]
    metodo_pagamento = models.CharField(max_length=10, choices=PAGAMENTO_OPCOES)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.cpf})"

class Apadrinhamento(models.Model):
    padrinho = models.ForeignKey(Padrinho, on_delete=models.CASCADE)
    crianca = models.ForeignKey(Crianca, on_delete=models.CASCADE)
    data_apadrinhamento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.padrinho.nome} apadrinhou {self.crianca.nome}"
