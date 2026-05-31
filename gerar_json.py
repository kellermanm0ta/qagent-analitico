import json
import random
from datetime import datetime, timedelta


def generate_random_execution(i):
    total = random.randint(50, 200)
    falhas = random.randint(0, 15)

    if falhas == 0:
        status = "SUCESSO"
    elif falhas < 5:
        status = "PARCIAL"
    else:
        status = "FALHA"

    sucesso = total - falhas

    # Generate random date within the last 30 days
    date = datetime.now() - timedelta(
        days=random.randint(0, 30), hours=random.randint(0, 23)
    )

    logs = []
    if falhas > 0:
        for j in range(random.randint(1, falhas)):
            arquivos = [
                "test_auth.py",
                "test_models.py",
                "test_views.py",
                "test_api.py",
                "test_services.py",
            ]
            erros = [
                "AssertionError: expected 200 but got 404",
                "IndexError: list index out of range",
                "TypeError: unhashable type: 'dict'",
                "ValueError: invalid literal for int() with base 10",
                "KeyError: 'user_id'",
            ]
            logs.append(
                {"arquivo": random.choice(arquivos), "mensagem": random.choice(erros)}
            )

    return {
        "data_execucao": date.isoformat(),
        "total_testes": total,
        "testes_sucesso": sucesso,
        "testes_falha": falhas,
        "tempo_execucao": round(random.uniform(5.0, 120.0), 2),
        "cobertura_codigo": round(random.uniform(60.0, 99.9), 2),
        "status": status,
        "logs": logs,
    }


registros = [generate_random_execution(i) for i in range(50)]

with open("dados_ingestao.json", "w") as f:
    json.dump(registros, f, indent=4)

print("Arquivo dados_ingestao.json gerado com sucesso com 50 registros.")
