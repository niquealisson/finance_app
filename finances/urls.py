# finances/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.listar_transacoes, name='listar_transacoes'),
    path('nova/', views.nova_transacao, name='nova_transacao'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('relatorio/', views.relatorio_transacoes, name='relatorio_transacoes'),
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('cadastrar_categoria/', views.cadastrar_categoria, name='cadastrar_categoria'),
    path('excluir/<int:pk>/', views.excluir_transacao, name='excluir_transacao'),
    path('editar/<int:pk>/', views.editar_transacao, name='editar_transacao'),
    path('categoria/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categoria/<int:pk>/excluir/', views.excluir_categoria, name='excluir_categoria'),
    path('login/', LoginView.as_view(template_name='finances/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('transacao/<int:pk>/', views.detalhes_transacao, name='detalhes_transacao'),
    path('detalhes_mes/<str:mes>/', views.detalhes_mes, name='detalhes_mes'),
]
