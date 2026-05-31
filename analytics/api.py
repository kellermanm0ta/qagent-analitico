from rest_framework import serializers, viewsets, mixins
from django.db import transaction
from .models import ExecucaoTeste, LogErro

class LogErroSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogErro
        fields = ['arquivo', 'mensagem']

class ExecucaoTesteSerializer(serializers.ModelSerializer):
    logs = LogErroSerializer(many=True, required=False)

    class Meta:
        model = ExecucaoTeste
        fields = [
            'data_execucao',
            'total_testes',
            'testes_sucesso',
            'testes_falha',
            'tempo_execucao',
            'cobertura_codigo',
            'status',
            'logs'
        ]

    def create(self, validated_data):
        logs_data = validated_data.pop('logs', [])
        
        with transaction.atomic():
            execucao = ExecucaoTeste.objects.create(**validated_data)
            
            for log_data in logs_data:
                LogErro.objects.create(execucao=execucao, **log_data)
                
        return execucao

class ExecucaoTesteViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet restrito apenas para a criação de novas ExecucaoTeste.
    Permite criação em lote (lista) ou única.
    """
    queryset = ExecucaoTeste.objects.all()
    serializer_class = ExecucaoTesteSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)
