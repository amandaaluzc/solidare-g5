from django.urls import path
from . import views

urlpatterns = [
    path('' , views.homepage , name='home'),
    path('apadrinhamento/', views.lista_criancas, name='lista_criancas')
]
