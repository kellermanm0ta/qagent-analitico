from django.contrib import admin
from .models import ExecucaoTeste, LogErro

@admin.register(ExecucaoTeste)
class ExecucaoTesteAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_execucao', 'status', 'total_testes', 'testes_sucesso', 'testes_falha', 'cobertura_codigo')
    list_filter = ('status', 'data_execucao')
    search_fields = ('id',)

@admin.register(LogErro)
class LogErroAdmin(admin.ModelAdmin):
    list_display = ('id', 'execucao', 'arquivo', 'criado_em')
    list_filter = ('criado_em',)
    search_fields = ('arquivo', 'mensagem')

