from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Padrinho

class PadrinhoRegistrationForm(forms.Form):
    # Dados de login / usuário -----------------
    first_name      = forms.CharField(label="Nome",  max_length=30)
    last_name       = forms.CharField(label="Sobrenome", max_length=150)
    email           = forms.EmailField(label="E‑mail")
    password1       = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2       = forms.CharField(label="Confirme a senha", widget=forms.PasswordInput)

    # Dados de padrinho -------------------------
    telefone        = forms.CharField(label="Telefone", max_length=20)
    cpf             = forms.CharField(label="CPF", max_length=14)
    metodo_pagamento = forms.ChoiceField(
        label="Método de pagamento",
        choices=Padrinho.PAGAMENTO_OPCOES
    )

    # -------- Validações --------
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("Já existe um usuário com este e‑mail.")
        return email

    def clean(self):
        super().clean()
        if self.cleaned_data.get("password1") != self.cleaned_data.get("password2"):
            self.add_error("password2", "As senhas não conferem.")
