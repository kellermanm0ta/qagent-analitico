from django.db import models

class ExecucaoTeste(models.Model):
    STATUS_CHOICES = [
        ('SUCESSO', 'Sucesso'),
        ('FALHA', 'Falha'),
        ('PARCIAL', 'Parcial')
    ]

    data_execucao = models.DateTimeField()
    total_testes = models.IntegerField()
    testes_sucesso = models.IntegerField()
    testes_falha = models.IntegerField()
    tempo_execucao = models.FloatField()
    cobertura_codigo = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Execução #{self.id} - {self.data_execucao.strftime('%d/%m/%Y %H:%M')} - {self.status}"

class LogErro(models.Model):
    execucao = models.ForeignKey(ExecucaoTeste, on_delete=models.CASCADE, related_name='logs')
    arquivo = models.CharField(max_length=255)
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Erro na Execução #{self.execucao.id} - {self.arquivo}"

