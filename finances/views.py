from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from django.shortcuts import render
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from .models import Transacao, Categoria
from django.db.models.functions import TruncMonth
from .forms import TransacaoForm
from .models import Categoria
from django.core.paginator import Paginator
from .forms import CategoriaForm
from decimal import Decimal
from datetime import datetime
from dateutil.relativedelta import relativedelta

def dashboard(request):
    # Recuperar todas as transações do banco de dados
    transacoes = Transacao.objects.all()

    # Calcular entradas e saídas
    total_entradas = sum(transacao.valor for transacao in transacoes if transacao.tipo == 'entrada')
    total_saidas = sum(transacao.valor for transacao in transacoes if transacao.tipo == 'saida')

    # Agrupar saídas por categoria
    gastos_por_categoria = defaultdict(Decimal)
    for transacao in transacoes.filter(tipo='saida'):
        gastos_por_categoria[transacao.categoria.nome] += transacao.valor

    # Calcular saldo e indicadores financeiros
    saldo = total_entradas - total_saidas
    percentual_economia = (saldo / total_entradas * 100) if total_entradas > 0 else 0
    data_primeira_transacao = datetime(2024, 10, 1)  # Exemplo de data de início

# Data atual
    data_atual = datetime.now()

# Calcular a diferença em meses
    diferenca = relativedelta(data_atual, data_primeira_transacao)
    num_mes = diferenca.years * 12 + diferenca.months

# Se não houver transações, evita a divisão por zero
    num_mes = num_mes if num_mes > 0 else 1

# Calcular a média de saídas mensais
    media_saidas_mensais = total_saidas / num_mes
    saldo_esperado = saldo * Decimal('1.02')  # Exemplo de 10% de aumento no saldo

    # Recuperar as últimas transações (últimos 5 registros, por exemplo)
    ultimas_transacoes = transacoes.order_by('-data')[:5]

    # Converter defaultdict para um dicionário normal
    gastos_por_categoria = dict(gastos_por_categoria)

    # Enviar os dados para o template
    context = {
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'saldo': saldo,
        'percentual_economia': percentual_economia,
        'media_saidas_mensais': media_saidas_mensais,
        'saldo_esperado': saldo_esperado,
        'gastos_por_categoria': gastos_por_categoria,
        'ultimas_transacoes': ultimas_transacoes,
    }

    return render(request, 'finances/dashboard.html', context)
@login_required
def detalhes_mes(request, mes):
    ano, mes_num = mes.split('-')
    
    # Filtro das transações por mês
    entradas_mes = Transacao.objects.filter(tipo='entrada', data__year=ano, data__month=mes_num)
    saidas_mes = Transacao.objects.filter(tipo='saida', data__year=ano, data__month=mes_num)

    # Verificando se os filtros retornaram algo
    print(f'Entradas para {mes}:', entradas_mes)
    print(f'Saídas para {mes}:', saidas_mes)

    total_entradas = sum(t.valor for t in entradas_mes)
    total_saidas = sum(t.valor for t in saidas_mes)

    context = {
        'entradas_mes': entradas_mes,
        'saidas_mes': saidas_mes,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'mes': mes
    }

    return render(request, 'finances/detalhes_mes.html', context)
@login_required
def detalhes_transacao(request, pk):
    # Obter a transação específica com base no id (pk)
    transacao = get_object_or_404(Transacao, pk=pk)

    # Passar os dados da transação para o template
    return render(request, 'finances/detalhes_transacao.html', {
        'transacao': transacao,
    })
@login_required
def relatorio_transacoes(request):
    # Obter todas as transações
    transacoes = Transacao.objects.all()

    # Calcular o total de entradas
    total_entradas = sum(t.valor for t in transacoes if t.tipo == 'entrada')

    # Calcular o total de saídas
    total_saidas = sum(t.valor for t in transacoes if t.tipo == 'saida')

    # Calcular o total geral (entradas - saídas)
    total = total_entradas - total_saidas

    # Agrupar entradas por mês
    entradas_por_mes = (
        transacoes.filter(tipo='entrada')
        .annotate(mes=TruncMonth('data'))
        .values('mes')
        .annotate(total=Sum('valor'))
        .order_by('mes')
    )

    # Agrupar saídas por mês
    saidas_por_mes = (
        transacoes.filter(tipo='saida')
        .annotate(mes=TruncMonth('data'))
        .values('mes')
        .annotate(total=Sum('valor'))
        .order_by('mes')
    )

    # Passar os totais e as transações para o template
    return render(request, 'finances/relatorio_transacoes.html', {
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'total': total,
        'entradas_por_mes': entradas_por_mes,
        'saidas_por_mes': saidas_por_mes,
    })
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

    # Agrupar entradas por mês
    entradas_por_mes = (
        transacoes.filter(tipo='entrada')
        .annotate(mes=TruncMonth('data'))
        .values('mes')
        .annotate(total=Sum('valor'))
        .order_by('mes')
    )

    # Agrupar saídas por mês
    saidas_por_mes = (
        transacoes.filter(tipo='saida')
        .annotate(mes=TruncMonth('data'))
        .values('mes')
        .annotate(total=Sum('valor'))
        .order_by('mes')
    )

    # Paginando as transações - 10 transações por página
    paginator = Paginator(transacoes, 5)  # 10 transações por página
    page_number = request.GET.get('page')  # Obtém o número da página da URL
    page_obj = paginator.get_page(page_number)

    # Passar os totais, as transações paginadas e os dados de agrupamento para o template
    return render(request, 'finances/listar_transacoes.html', {
        'page_obj': page_obj,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'total': total,
        'entradas_por_mes': entradas_por_mes,
        'saidas_por_mes': saidas_por_mes,
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