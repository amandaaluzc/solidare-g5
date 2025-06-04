from django.urls import path
from . import views

urlpatterns = [
    path("criança/<int:crianca_id>/", views.detalhes_crianca, name="detalhes_crianca"),
    path("cadastro-padrinho/", views.registrar_padrinho, name="cadastro_padrinho"),
    path('' , views.homepage, name='home'),
    path('lista-criancas/', views.lista_criancas, name='lista_criancas'),
    path('pagina-exibicao/', views.pagina_exibicao, name='pagina_exibicao'),
    path('pagamento', views.pagamento, name='pagamento'),
]
