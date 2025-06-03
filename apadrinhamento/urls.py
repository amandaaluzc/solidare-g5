from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("criança/<int:crianca_id>/", views.detalhes_crianca, name="detalhes_crianca"),
    path('login/', views.login_padrinho, name='login_padrinho'),
    path('logout/', views.logout_view, name='logout_padrinho'),
    path('registrar/', views.registrar_padrinho, name='registrar_padrinho'),
    path('painel-admin/', login_required(views.admin), name='painel_admin'),
    path('' , views.homepage, name='home'),
    path('criancas/cadastrar/', views.cadastrar_crianca, name='cadastrar_crianca'),
    path('lista-criancas/', views.lista_criancas, name='lista_criancas'),
    path('pagina-exibicao/', views.pagina_exibicao, name='pagina_exibicao'),
    path('login_admin/' , views.login_admin , name='login_admin'),
    path('escolha_adm/' , login_required(views.escolha_admin) , name= 'escolha_admin'),
    path('apadrinhar/<int:crianca_id>/', views.apadrinhar_crianca, name='apadrinhar_crianca'),
    path('criancas/<int:crianca_id>/editar/', views.editar_crianca, name='editar_crianca'),
    path('criancas/<int:crianca_id>/excluir/', views.deletar_crianca, name='deletar_crianca'),
    path ('gerenciar_padrinhos/' , login_required(views.gerenciar_padrinhos) , name='gerenciar_padrinhos'),
    path ('gerenciar_afilhados/' , login_required(views.gerenciar_afilhados) , name='gerenciar_afilhados'),
]
