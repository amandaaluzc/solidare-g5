from django.shortcuts import render
from .models import Crianca

def lista_criancas(request):
    criancas = Crianca.objects.all()
    return render(request, 'apadrinhamento/lista_criancas.html', {'criancas': criancas})
