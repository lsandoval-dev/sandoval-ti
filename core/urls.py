from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
path('', views.home, name='home'),


# Autenticação
path(
    'login/',
    auth_views.LoginView.as_view(
        template_name='login.html'
    ),
    name='login'
),

path(
    'logout/',
    auth_views.LogoutView.as_view(),
    name='logout'
),

# Clientes
path('clientes/', views.clientes, name='clientes'),
path('clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
path('clientes/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),

# Ordens de Serviço
path('ordens/', views.ordens, name='ordens'),
path('ordens/nova/', views.nova_ordem, name='nova_ordem'),
path('ordens/detalhar/<int:id>/', views.detalhar_ordem, name='detalhar_ordem'),
path('ordens/imprimir/<int:id>/', views.imprimir_ordem, name='imprimir_ordem'),
path('ordens/editar/<int:id>/', views.editar_ordem, name='editar_ordem'),
path('ordens/excluir/<int:id>/', views.excluir_ordem, name='excluir_ordem'),

# Dashboard
path('dashboard/', views.dashboard, name='dashboard'),

# Usuários
path('usuarios/', views.usuarios, name='usuarios'),
path(
    'usuarios/editar/<int:id>/',
    views.editar_usuario,
    name='editar_usuario'
),
path(
    'usuarios/excluir/<int:id>/',
    views.excluir_usuario,
    name='excluir_usuario'
),

# Acesso negado
path('acesso-negado/', views.acesso_negado, name='acesso_negado'),

]