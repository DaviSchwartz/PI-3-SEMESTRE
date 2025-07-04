from django.contrib import admin
from django.urls import path
from Sistema import views
from django.conf import settings
from django.conf.urls.static import static

from Sistema.views import (
    home, login,
    cadastrar_restaurante,
    cadastro_colaborador,
    cadastrar_usuario,
    editar_restaurante,
    excluir_restaurante)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastrar-restaurante/', cadastrar_restaurante, name='cadastrar-restaurante'),
    path('editar-restaurante/<int:id>/', editar_restaurante, name='editar-restaurante'),
    path('excluir-restaurante/<int:id>/', excluir_restaurante, name='excluir-restaurante'),
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('cadastro/', cadastro_colaborador, name='cadastro'),
    path('cadastrar-usuario/', cadastrar_usuario, name='cadastrar_usuario'),
    path('relatorio/', views.relatorio, name='relatorio'), 
    path('listar-restaurantes/', views.listar_restaurantes, name='listar-restaurantes'),
    path('listar-obras/', views.listar_obras, name='listar-obras'),
    path('cadastrar-obra/', views.cadastro_obras, name='cadastrar-obra'), 
    path('editar-obra/<int:id>/', views.editar_obra, name='editar-obra'),
    path('obra/<int:id>/detalhes/', views.detalhes_obra, name='detalhes-obra'),
    path('listar-colaboradores/', views.lista_colaboradores, name='listar-colaboradores'),
    path('editar-colaborador/<int:id>/', views.editar_colaborador, name='editar-colaborador'),
    path('excluir-colaborador/<int:id>/', views.excluir_colaborador, name='excluir-colaborador'),
    path('listar-hoteis/', views.listar_hoteis, name='listar-hoteis'), 
    path('cadastrar-hotel/', views.cadastro_hotel, name='cadastrar-hotel'), 
    path('deletar/', views.deletar_generico, name='deletar-generico'),
    path('editar-hotel/<int:id>/', views.editar_hotel, name='editar-hotel'),
    path('editar/', views.redirecionar_edicao_hotel, name='redirecionar-edicao-hotel'),
    path('listar-pedidos/', views.listar_pedidos, name='listar_pedidos'),
    path('cadastrar-pedido/', views.cadastrar_pedido, name='cadastrar_pedido'),
    path('refeicoes/registros/', views.listar_registros, name='listar_registros'),
    path('refeicoes/editar/<str:registro_id>/', views.editar_registro, name='editar_registro'),
    path('refeicoes/excluir/<str:registro_id>/', views.excluir_registro, name='excluir_registro'),
    path('dashboard/', views.relatorio, name='relatorio'),

    #path('editar-pedido/<str:pedido_id>/', views.editar_pedido, name='editar_pedido'),
    #path('excluir-pedido/<str:pedido_id>/', views.excluir_pedido, name='excluir_pedido'),    
]
