from django.urls import path
from . import views

app_name = 'medicos'

urlpatterns = [
    path('registro/medico/', views.medico_cadastro, name='medico_cadastro'),
    path('agendar/', views.agenda_cadastro, name='agendar_consulta'),
    path('agendar/atualizar/<int:pk>/', views.agenda_atualizar, name='agendar_consulta_atualizar'),
    path('agendar/apagar/<int:pk>/', views.agenda_deletar, name='agendar_consulta_deletar'),
    path('minhas/consultas/', views.agenda_lista, name="agenda_lista"),
    path('admim/lista/medicos/', views.medico_lista, name="medicos_lista"),
    path('registro/especialidade/', views.especialidade_cadastro, name='especialidade_cadastro'),
    path('admim/lista/especialidades/', views.especialidade_lista, name="especialidade_lista"),
    path('especialidade/atualizar/<int:pk>/', views.especialidade_atualizar, name='especialidade_cadastro_atualizar'),
    path('especialidade/apagar/<int:pk>/', views.especialidade_deletar, name='especialidade_deletar'),
    path('relatorio-medicos/', views.relatorio_medicos, name='relatorio_medicos')
]