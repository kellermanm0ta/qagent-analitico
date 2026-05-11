from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from .models import ExecucaoTeste, LogErro

@login_required
def dashboard(request):
    execucoes = ExecucaoTeste.objects.all()
    
    total_execucoes = execucoes.count()
    taxa_sucesso = execucoes.filter(status='SUCESSO').count()
    
    agregados = execucoes.aggregate(
        avg_cobertura=Avg('cobertura_codigo'),
        total_testes=Sum('total_testes'),
        total_sucesso=Sum('testes_sucesso'),
        total_falha=Sum('testes_falha')
    )
    
    context = {
        'total_execucoes': total_execucoes,
        'taxa_sucesso': taxa_sucesso,
        'agregados': agregados,
        'ultimas_execucoes': execucoes.order_by('-data_execucao')[:5]
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def lista_execucoes(request):
    execucoes = ExecucaoTeste.objects.all().order_by('-data_execucao')
    return render(request, 'dashboard/lista_execucoes.html', {'execucoes': execucoes})

@login_required
def detalhe_execucao(request, id):
    execucao = get_object_or_404(ExecucaoTeste, id=id)
    logs = execucao.logs.all().order_by('-criado_em')
    return render(request, 'dashboard/detalhe_execucao.html', {'execucao': execucao, 'logs': logs})

