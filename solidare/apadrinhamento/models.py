from django.db import models

class Crianca(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    descricao = models.TextField()

    def __str__(self):
        return self.nome

class Padrinho(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    metodo_pagamento = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Apadrinhamento(models.Model):
    padrinho = models.ForeignKey(Padrinho, on_delete=models.CASCADE)
    crianca = models.ForeignKey(Crianca, on_delete=models.CASCADE)
    data_apadrinhamento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.padrinho.nome} apadrinhou {self.crianca.nome}"
