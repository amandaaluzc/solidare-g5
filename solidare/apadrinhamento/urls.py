from django.urls import path
from . import views

urlpatterns = [
    path('' , views.homepage),
    path('apadrinhamento/', views.lista_criancas, name='lista_criancas')
]
