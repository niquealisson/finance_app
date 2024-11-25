from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_transacoes, name='listar_transacoes'),
    path('nova/', views.nova_transacao, name='nova_transacao'),
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('cadastrar_categoria/', views.cadastrar_categoria, name='cadastrar_categoria'),
    path('excluir/<int:pk>/', views.excluir_transacao, name='excluir_transacao'),
    path('editar/<int:pk>/', views.editar_transacao, name='editar_transacao'),
    path('categoria/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categoria/<int:pk>/excluir/', views.excluir_categoria, name='excluir_categoria'),
]
