from django.urls import path
from . import views

urlpatterns = [
    path("criança/<int:crianca_id>/", views.detalhes_crianca, name="detalhes_crianca"),
    path('login/', views.login_padrinho, name='login_padrinho'),
    path('logout/', views.logout_view, name='logout_padrinho'),
    path('registrar/', views.registrar_padrinho, name='registrar_padrinho'),
    path('painel-admin/', views.admin, name='painel_admin'),
    path('' , views.homepage, name='home'),
    path('lista-criancas/', views.lista_criancas, name='lista_criancas'),
    path('pagina-exibicao/', views.pagina_exibicao, name='pagina_exibicao'),
    path ('login_admin/' , views.login_admin , name='login_admin'),
]
