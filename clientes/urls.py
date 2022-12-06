from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('registro/', views.cliente_cadastro, name='cliente_cadastro'),
    path('atualizar/', views.cliente_atualizar, name='cliente_atualizar'),
    path('consultas/', views.consulta_lista, name='consulta_list'),
    path('consultas/criar/', views.consulta_cadastro, name='consulta_create'),
    path('consultas/editar/<int:pk>/', views.consulta_atualizar, name='consulta_update'),
    path('consultas/excluir/<int:pk>/', views.consulta_excluir, name='consulta_delete'),
    path('registro/plano/', views.plano_cadastro, name='plano_cadastro'),
    path('admim/lista/planos/', views.plano_lista, name='plano_lista'),
    path('plano/excluir/<int:pk>', views.plano_excluir, name='plano_delete'),
]
