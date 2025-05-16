from django.shortcuts import render, redirect
from .models import Crianca
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


from django.contrib.auth import authenticate, login

from .forms import PadrinhoRegistrationForm
from .models import Padrinho , Apadrinhamento

def registrar_padrinho(request):
    if request.method == "POST":
        form = PadrinhoRegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # 1) criar usuário
                    user = User.objects.create_user(
                        username=form.cleaned_data["email"],   # username = email
                        email=form.cleaned_data["email"],
                        password=form.cleaned_data["password1"],
                        first_name=form.cleaned_data["first_name"],
                        last_name=form.cleaned_data["last_name"],
                    )

                    # 2) criar padrinho vinculado
                    Padrinho.objects.create(
                        user=user,
                        telefone=form.cleaned_data["telefone"],
                        cpf=form.cleaned_data["cpf"],
                        metodo_pagamento=form.cleaned_data["metodo_pagamento"],
                    )
                messages.success(request, "Cadastro realizado com sucesso! Você já pode fazer login.")
                return redirect("home")   # ajuste para a sua rota de login
            except Exception:
                messages.error(request, "Erro inesperado ao salvar. Tente novamente.")
    else:
        form = PadrinhoRegistrationForm()

    return render(request, "registrar_padrinho.html", {"form": form})


def lista_criancas(request):
    criancas = Crianca.objects.all()
    return render(request, 'lista_criancas.html', {'criancas': criancas})

def homepage (request):
    return render (request , 'home.html')

def detalhes_crianca(request, crianca_id):
    crianca = get_object_or_404(Crianca, id=crianca_id)
    return render(request, "detalhes_crianca.html", {"crianca": crianca})

def pagina_exibicao(request):
    criancas = Crianca.objects.all()
    return render(request, 'pagina_exibição.html', {'criancas': criancas})

def login_padrinho(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('password')
        user = authenticate(request, username=email, password=senha)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email ou senha incorretos.')

    return render(request, 'login_padrinho.html')

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def admin(request):
    if not request.user.is_staff:
        if not request.user.is_staff:
            return HttpResponseForbidden("Acesso restrito a administradores.")
    
    return render(request, 'painel_admin.html')

@login_required
def escolha_admin(request):
    if not request.user.is_staff:
        if not request.user.is_staff:
            return HttpResponseForbidden("Acesso restrito a administradores.")
    
    return render(request, 'escolha_admin.html')




def login_admin(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('password')
        
        user = authenticate(request, username=nome, password=senha)
        
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('escolha_admin')
            else:
                messages.error(request, 'Apenas o superusuário pode acessar este painel.')
        else:
            messages.error(request, 'Nome ou senha incorretos.')

    return render(request, 'login_adm.html')

@login_required
def gerenciar_padrinhos (request):
    if not request.user.is_staff:
        if not request.user.is_staff:
            return HttpResponseForbidden("Acesso restrito a administradores.")
    
    padrinhos = Padrinho.objects.all()
    apadrinhamentos = Apadrinhamento.objects.select_related('padrinho__user', 'crianca')
    
    return render(request, 'gerenciar_padrinho.html' , {'padrinhos': padrinhos ,  'apadrinhamentos': apadrinhamentos})

@login_required
def gerenciar_afilhados (request):
    if not request.user.is_staff:
        if not request.user.is_staff:
            return HttpResponseForbidden("Acesso restrito a administradores.")
    
    return render(request, 'gerenciar_afilhado.html')

