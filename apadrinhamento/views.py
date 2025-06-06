from django.shortcuts import render, redirect
from .models import Crianca, Apadrinhamento, Padrinho
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Padrinho 
from django.conf import settings


from django.contrib.auth import authenticate, login

from .forms import PadrinhoRegistrationForm
from .forms import CriancaForm

@csrf_exempt
@require_POST
def limpar_dados_geral(request):
    if not settings.DEBUG:
        return JsonResponse({'error': 'Acesso negado'}, status=403)

    
    Apadrinhamento.objects.all().delete()
    Crianca.objects.all().delete()

    
    usuarios_de_teste = User.objects.filter(email__icontains='@email.com', is_staff=False)
    Padrinho.objects.filter(user__in=usuarios_de_teste).delete()
    usuarios_de_teste.delete()

    return JsonResponse({'status': 'dados limpos com sucesso'})



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
    # oculta crianças que já têm padrinho
    ids_apadrinhadas = Apadrinhamento.objects.values_list("crianca_id", flat=True)
    criancas = Crianca.objects.exclude(id__in=ids_apadrinhadas)
    return render(request, 'lista_criancas.html', {'criancas': criancas})

def homepage (request):
    total_afilhados = Crianca.objects.count()
    
    afilhados_apadrinhados = Apadrinhamento.objects.values('crianca').distinct().count()
    afilhados_disponiveis = total_afilhados - afilhados_apadrinhados
    
    
    labels = ['Crianças apadrinhadas', 'Total de crianças']
    data = [afilhados_apadrinhados, total_afilhados]
    
    
    conteudo = {
        'labels': labels,
        'data': data,
    }
    
    
    return render (request , 'home.html', conteudo)

def detalhes_crianca(request, crianca_id):
    crianca = get_object_or_404(Crianca, id=crianca_id)
    # verifica se já há apadrinhamento
    apadrinhada = Apadrinhamento.objects.filter(crianca=crianca).exists()
    return render(
        request,
        "detalhes_crianca.html",
        {"crianca": crianca, "apadrinhada": apadrinhada},
    )
def pagina_exibicao(request):
    # exibe apenas crianças ainda sem padrinho
    ids_apadrinhadas = Apadrinhamento.objects.values_list("crianca_id", flat=True)
    criancas = Crianca.objects.exclude(id__in=ids_apadrinhadas)
    return render(request, 'pagina_exibição.html', {'criancas': criancas})

def login_padrinho(request):
    next_url = request.GET.get('next', 'home')  # pega o 'next' da URL, ou 'home' como padrão

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('password')
        user = authenticate(request, username=email, password=senha)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next', 'home')  # garante que 'next' do POST também é considerado
            return redirect(next_url)
        else:
            messages.error(request, 'Email ou senha incorretos.')

    return render(request, 'login_padrinho.html', {
        'next': next_url
    })

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def admin(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso restrito a administradores.")
    
    return render(request, 'painel_admin.html')

@login_required
def escolha_admin(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso restrito a administradores.")
    
    return render(request, 'escolha_admin.html')


def login_admin(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('password')
        
        user = authenticate(request, username=nome, password=senha)
        
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('escolha_admin')
            else:
                messages.error(request, 'Apenas adms do site podem acessar este painel.')
        else:
            messages.error(request, 'Nome ou senha incorretos.')

    return render(request, 'login_adm.html')

@login_required
def gerenciar_padrinhos (request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso restrito a administradores.")
    
    padrinhos = Padrinho.objects.all()
    apadrinhamentos = Apadrinhamento.objects.select_related('padrinho__user', 'crianca')
    
    return render(request, 'gerenciar_padrinho.html' , {'padrinhos': padrinhos ,  'apadrinhamentos': apadrinhamentos})

@login_required
def gerenciar_afilhados(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso restrito a administradores.")
    
    padrinhos = Padrinho.objects.all()
    
    apadrinhamentos_existentes = Apadrinhamento.objects.select_related('padrinho__user', 'crianca')
    

    todas_criancas = Crianca.objects.all()
    
   
    apadrinhamentos = []
    criancas_apadrinhadas_ids = set(ap.crianca.id for ap in apadrinhamentos_existentes)
    

    for ap in apadrinhamentos_existentes:
        apadrinhamentos.append(ap)
    

    for crianca in todas_criancas:
        if crianca.id not in criancas_apadrinhadas_ids:
            ap_vazio = Apadrinhamento(crianca=crianca, padrinho=None)
            apadrinhamentos.append(ap_vazio)
    
    return render(request, 'gerenciar_afilhado.html', {'padrinhos': padrinhos, 'apadrinhamentos': apadrinhamentos})

@login_required
def apadrinhar_crianca(request, crianca_id):
    try:
        padrinho = request.user.padrinho
    except Padrinho.DoesNotExist:
        return HttpResponseForbidden("Somente usuários do tipo padrinho podem apadrinhar uma criança.")
    
    crianca = get_object_or_404(Crianca, id=crianca_id)

    if Apadrinhamento.objects.filter(crianca=crianca).exists():
        messages.error(request, "Esta criança já foi apadrinhada por outro usuário.")
        return redirect('pagina_exibicao')
    
    Apadrinhamento.objects.create(padrinho=padrinho, crianca=crianca)
    messages.success(request, "Apadrinhamento realizado com sucesso!")
    return redirect('pagina_exibicao')


@login_required
def cadastrar_crianca(request):
    if request.method == "POST":
        form = CriancaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Criança cadastrada com sucesso!")
            return redirect('gerenciar_afilhados')
    else:
        form = CriancaForm()

    return render(request, "cadastrar_crianca.html", {"form": form})

@login_required
def deletar_crianca(request, crianca_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso restrito a administradores.")

    crianca = get_object_or_404(Crianca, id=crianca_id)
    Apadrinhamento.objects.filter(crianca=crianca).delete()

    crianca.delete()
    messages.success(request, f"Criança “{crianca.nome}” excluída com sucesso.")
    return redirect('gerenciar_afilhados')

def editar_crianca(request, crianca_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso restrito a administradores.")

    crianca = get_object_or_404(Crianca, id=crianca_id)

    if request.method == "POST":
        form = CriancaForm(request.POST, request.FILES, instance=crianca)
        if form.is_valid():
            form.save()
            messages.success(request, f"Criança “{crianca.nome}” atualizada com sucesso!")
            return redirect('gerenciar_afilhados')
        else:
            messages.error(request, "Não foi possível atualizar. Verifique os dados.")
            return redirect('gerenciar_afilhados')
    else:
        return redirect('gerenciar_afilhados')

@require_POST
@login_required
def deletar_padrinho(request, padrinho_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Acesso restrito.")

    padrinho = get_object_or_404(Padrinho, id=padrinho_id)
    user = padrinho.user

    padrinho.delete()
    user.delete()
    return JsonResponse({'success': True})

@csrf_exempt
@require_POST
def editar_padrinho(request, padrinho_id):
    try:
        padrinho = Padrinho.objects.get(id=padrinho_id)
        
        padrinho.user.first_name = request.POST.get('nome', '').split(' ')[0]
        if ' ' in request.POST.get('nome', ''):
            padrinho.user.last_name = request.POST.get('nome', '').split(' ')[1]
        padrinho.user.email = request.POST.get('email', '')
        padrinho.telefone = request.POST.get('telefone', '')
        
        padrinho.user.save()
        padrinho.save()
        
        return JsonResponse({'success': True})
    except Padrinho.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Padrinho não encontrado'}, status=404)
    

def api_padrinho(request, padrinho_id):
    try:
        padrinho = Padrinho.objects.get(id=padrinho_id)
        data = {
            'user': {
                'first_name': padrinho.user.first_name,
                'last_name': padrinho.user.last_name,
                'email': padrinho.user.email,
            },
            'telefone': padrinho.telefone
        }
        return JsonResponse(data)
    except Padrinho.DoesNotExist:
        return JsonResponse({'error': 'Padrinho não encontrado'}, status=404)

@login_required
def pagina_pagamento(request, id):
    crianca = get_object_or_404(Crianca, id=id)
    return render(request, 'pagina_pagamento.html', {'crianca': crianca})

@login_required
def confirmar_apadrinhamento(request, id):
    if request.method == 'POST':
        crianca = get_object_or_404(Crianca, id=id)

        Apadrinhamento.objects.create(crianca=crianca)

        return redirect('pagina_exibição')