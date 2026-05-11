import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from analytics.models import ExecucaoTeste, LogErro

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("Superuser 'admin' criado com senha 'admin'.")

if not ExecucaoTeste.objects.exists():
    now = timezone.now()
    e1 = ExecucaoTeste.objects.create(
        data_execucao=now - timedelta(days=2),
        total_testes=50,
        testes_sucesso=50,
        testes_falha=0,
        tempo_execucao=12.5,
        cobertura_codigo=85.0,
        status='SUCESSO'
    )
    e2 = ExecucaoTeste.objects.create(
        data_execucao=now - timedelta(days=1),
        total_testes=55,
        testes_sucesso=52,
        testes_falha=3,
        tempo_execucao=15.2,
        cobertura_codigo=86.5,
        status='FALHA'
    )
    LogErro.objects.create(execucao=e2, arquivo='tests/test_auth.py', mensagem='AssertionError: False is not True\n  File "tests/test_auth.py", line 42, in test_login')
    LogErro.objects.create(execucao=e2, arquivo='tests/test_models.py', mensagem='IntegrityError: UNIQUE constraint failed: auth_user.username')
    
    e3 = ExecucaoTeste.objects.create(
        data_execucao=now,
        total_testes=60,
        testes_sucesso=59,
        testes_falha=1,
        tempo_execucao=14.8,
        cobertura_codigo=88.2,
        status='PARCIAL'
    )
    LogErro.objects.create(execucao=e3, arquivo='tests/test_views.py', mensagem='Http404: No MyModel matches the given query.')
    print("Dados fictícios criados para visualização do dashboard.")
