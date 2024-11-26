from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Transacao, Categoria
from .forms import TransacaoForm
from .models import Categoria
from .forms import CategoriaForm

@login_required
def listar_transacoes(request):
    # Obter todas as transações
    transacoes = Transacao.objects.all()

    # Calcular o total de entradas
    total_entradas = sum(t.valor for t in transacoes if t.tipo == 'entrada')

    # Calcular o total de saídas
    total_saidas = sum(t.valor for t in transacoes if t.tipo == 'saida')

    # Calcular o total geral (entradas - saídas)
    total = total_entradas - total_saidas

    # Passar os totais e as transações para o template
    return render(request, 'finances/listar_transacoes.html', {
        'transacoes': transacoes,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'total': total,
    })
@login_required
def nova_transacao(request):
    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_transacoes')  # Redireciona para a lista de transações
    else:
        form = TransacaoForm()
    return render(request, 'finances/nova_transacao.html', {'form': form})
@login_required
def cadastrar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')  # Redireciona para a lista de categorias
    else:
        form = CategoriaForm()
    return render(request, 'finances/cadastrar_categoria.html', {'form': form})
@login_required
def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'finances/listar_categorias.html', {'categorias': categorias})
@login_required
def excluir_transacao(request, pk):
    # Obtém a transação com base no ID (pk)
    transacao = get_object_or_404(Transacao, pk=pk)

    # Verifica se a requisição é do tipo POST (confirmação de exclusão)
    if request.method == 'POST':
        transacao.delete()  # Deleta a transação
        return redirect('listar_transacoes')  # Redireciona para a listagem de transações

    return render(request, 'finances/excluir_transacao.html', {'transacao': transacao})
@login_required
def editar_transacao(request, pk):
    # Obtém a transação com base no ID (pk)
    transacao = get_object_or_404(Transacao, pk=pk)

    # Se o método da requisição for POST, significa que o formulário foi enviado
    if request.method == 'POST':
        form = TransacaoForm(request.POST, instance=transacao)
        if form.is_valid():
            form.save()  # Atualiza a transação com os novos dados
            return redirect('listar_transacoes')  # Redireciona para a listagem de transações
    else:
        form = TransacaoForm(instance=transacao)  # Preenche o formulário com os dados da transação

    return render(request, 'finances/editar_transacao.html', {'form': form, 'transacao': transacao})
@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')  # Redireciona para a lista de categorias
    else:
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'finances/editar_categoria.html', {'form': form})
@login_required
def excluir_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    categoria.delete()
    return redirect('listar_categorias')