from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_criancas, name='lista_criancas'),
]
