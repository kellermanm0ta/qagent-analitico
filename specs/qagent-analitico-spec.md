# Especificação de Arquitetura — QAgent Analytics

# 1. Visão Geral da Arquitetura

## Objetivo

Definir a arquitetura da aplicação web QAgent Analytics, responsável por consumir dados analíticos armazenados em banco de dados e renderizar dashboards para monitoramento da atuação do QAgent.

Nesta evolução da aplicação:

* Não haverá cadastro de projetos via interface visual (apenas visualização);
* A aplicação atuará como uma camada de visualização e monitoramento dos dados analíticos;
* **Haverá uma API REST para ingestão de dados**, permitindo que o QAgent (ou outras ferramentas) envie os resultados das execuções e logs de erro diretamente para o banco de dados da aplicação;
* O dashboard continuará consumindo os dados diretamente do banco para renderização.

---

# 2. Arquitetura da Solução

A aplicação seguirá uma arquitetura monolítica simples baseada no padrão MTV (Model Template View) do Django.

## Camadas da Aplicação

```text
      ┌────────────────┐           ┌──────────────────────────┐
      │  Agente (QA)   │           │        Frontend          │
      │ Envia dados    │           │  HTML + Bootstrap 5      │
      └───────┬────────┘           └────────────┬─────────────┘
              │                                 │
              ▼ (POST)                          ▼ (GET)
┌──────────────────────────┐       ┌──────────────────────────┐
│        API REST          │       │      Django Views        │
│  (Django REST Framework) │       │  Regras de apresentação  │
└────────────┬─────────────┘       └────────────┬─────────────┘
             │                                  │
             ▼                                  ▼
┌──────────────────────────┐       ┌──────────────────────────┐
│      Django ORM          │       │      Django ORM          │
│  Gravação dos dados      │       │   Consulta aos dados     │
└────────────┬─────────────┘       └────────────┬─────────────┘
             │                                  │
             └───────────────┬──────────────────┘
                             ▼
               ┌──────────────────────────┐
               │      Banco de Dados      │
               │   Dados analíticos QA    │
               └──────────────────────────┘
```

---

# 3. Stack Tecnológica

## Backend

| Tecnologia            | Finalidade                           |
| --------------------- | ------------------------------------ |
| Python 3.12+          | Linguagem principal                  |
| Django 5+             | Framework web                        |
| Django REST Framework | Criação da API REST para ingestão    |
| Django ORM            | Persistência e consultas             |
| SQLite                | Banco local inicial                  |
| PostgreSQL            | Evolução futura                      |

---

## Frontend

| Tecnologia       | Finalidade               |
| ---------------- | ------------------------ |
| HTML5            | Estrutura das páginas    |
| Bootstrap 5      | Estilização responsiva   |
| Django Templates | Renderização server-side |

---

# 4. Componentes Arquiteturais

# 4.1 Django Views

## Responsabilidades

As Views serão responsáveis por:

* Receber requisições HTTP;
* Validar autenticação;
* Consultar dados analíticos;
* Processar métricas;
* Renderizar templates HTML.

## Estratégia

Utilizar Function Based Views (FBV) para simplificar o projeto.

## Exemplo

```python
@login_required

def dashboard(request):
    execucoes = ExecucaoTeste.objects.all()

    total_execucoes = execucoes.count()

    context = {
        'total_execucoes': total_execucoes
    }

    return render(request, 'dashboard.html', context)
```

---

# 4.2 Django ORM

## Responsabilidades

O ORM será utilizado para:

* Leitura dos dados analíticos;
* Consultas agregadas;
* Filtros;
* Ordenação;
* Estatísticas.

## Benefícios

* Evita SQL Injection;
* Simplifica consultas;
* Facilita manutenção;
* Integração nativa com Django.

---

# 4.3 Django Templates

## Objetivo

Renderização server-side dos dashboards.

## Estratégia

Utilizar templates reutilizáveis:

```text
templates/
│
├── base.html
├── login.html
└── dashboard/
    ├── index.html
    ├── metricas.html
    └── logs.html
```

---

# 4.4 Bootstrap

## Objetivo

Garantir:

* Responsividade;
* Layout simples;
* Componentização visual;
* Rapidez de desenvolvimento.

## Componentes Utilizados

* Navbar;
* Cards;
* Tables;
* Alerts;
* Forms;
* Buttons;
* Badges;
* Modals.

---

# 4.5 Django Authentication

## Objetivo

Controlar acesso ao dashboard.

## Estratégia

Utilizar autenticação nativa do Django.

## Recursos

* LoginView;
* LogoutView;
* Session Authentication;
* login_required.

---

# 4.6 Django Admin

## Objetivo

Permitir inspeção administrativa dos dados.

## Uso

* Consulta de execuções;
* Consulta de logs;
* Gestão de usuários.

---

# 4.7 API REST (Ingestão de Dados)

## Objetivo

Prover endpoints para que o agente de qualidade (QAgent) ou sistemas externos possam registrar automaticamente os resultados das execuções de testes e seus logs.

## Estratégia

Utilizar o Django REST Framework (DRF) para criar rotas seguras que recebam os payloads em formato JSON e os persistam via ORM.

## Autenticação da API

* Autenticação via Token (TokenAuthentication do DRF) para garantir que apenas agentes autorizados possam enviar dados.

## Endpoints Principais

* `POST /api/v1/execucoes/` — Registra execuções de teste (suporta tanto um único objeto quanto uma lista/array de execuções) e, opcionalmente, recebe de forma aninhada os logs de erro associados a cada execução.

---

# 5. Estrutura do Projeto

```text
qagent_analytics/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── analytics/
│   ├── models.py
│   ├── views.py
│   ├── api.py
│   ├── urls.py
│   ├── admin.py
│   ├── services.py
│   ├── templates/
│   ├── static/
│   └── migrations/
│
└── templates/
    ├── base.html
    ├── login.html
    └── dashboard/
```

---

# 6. Arquitetura de Dados

# Entidade Principal — ExecucaoTeste

Representa execuções realizadas pelo QAgent.

```python
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
```

---

# Entidade Secundária — LogErro

Representa logs gerados durante falhas.

```python
class LogErro(models.Model):
    execucao = models.ForeignKey(ExecucaoTeste, on_delete=models.CASCADE)
    arquivo = models.CharField(max_length=255)
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
```

---

# 7. Fluxo Arquitetural

## Fluxo de Consulta (Usuário no Dashboard)

```text
Usuário acessa dashboard
        ↓
Django URL Dispatcher
        ↓
Django View
        ↓
Consulta ORM
        ↓
Banco de Dados
        ↓
Processamento de métricas
        ↓
Template HTML
        ↓
Renderização Bootstrap
        ↓
Resposta HTTP
```

## Fluxo de Ingestão (QAgent via API)

```text
QAgent finaliza testes
        ↓
Gera payload JSON
        ↓
Requisição HTTP POST (com Token)
        ↓
Django URL Dispatcher (/api/v1/...)
        ↓
DRF ViewSet/APIView
        ↓
Validação via Serializer
        ↓
Gravação via Django ORM
        ↓
Banco de Dados
        ↓
Resposta HTTP 201 Created
```

---

# 8. Estrutura de URLs

```python
urlpatterns = [
    # URLs do Dashboard (Frontend)
    path('', views.dashboard, name='dashboard'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('execucoes/', views.lista_execucoes, name='lista_execucoes'),
    path('execucoes/<int:id>/', views.detalhe_execucao, name='detalhe_execucao'),
    
    # URLs da API REST (Ingestão)
    path('api/v1/execucoes/', api.ExecucaoTesteViewSet.as_view({'post': 'create'}), name='api_create_execucao'),
]
```

---

# 9. Estratégia de Renderização

## Tipo de Renderização

Server Side Rendering (SSR).

## Motivos

* Simplicidade;
* Menor complexidade;
* Melhor integração com Django;
* Facilidade acadêmica;
* Menor curva de manutenção.

---

# 10. Estratégia de Consultas

## Objetivo

As consultas deverão priorizar:

* Simplicidade;
* Legibilidade;
* Uso do ORM nativo.

## Exemplos

### Total de execuções

```python
ExecucaoTeste.objects.count()
```

### Taxa de sucesso

```python
ExecucaoTeste.objects.filter(status='SUCESSO').count()
```

### Cobertura média

```python
from django.db.models import Avg

ExecucaoTeste.objects.aggregate(
    Avg('cobertura_codigo')
)
```

---

# 11. Segurança da Aplicação

## Medidas Utilizadas

* Session Authentication;
* CSRF Protection;
* ORM contra SQL Injection;
* Rotas protegidas;
* Controle de sessão.

---

# 12. Estratégia de Responsividade

A interface deverá ser totalmente responsiva utilizando Bootstrap.

## Compatibilidade

* Desktop;
* Notebook;
* Tablet.

---

# 13. Escalabilidade Futura

A arquitetura deverá permitir evolução futura para:

* Dashboards em tempo real;
* Consumo externo por terceiros (ampliação das APIs REST);
* Gráficos interativos;
* WebSockets;
* Integração CI/CD;
* PostgreSQL;
* Docker.

---

# 14. Decisões Arquiteturais

| Decisão           | Motivo                     |
| ----------------- | -------------------------- |
| Django Monolítico | Simplicidade               |
| HTML Server Side  | Menor complexidade         |
| Bootstrap         | Rapidez visual             |
| ORM Nativo        | Segurança e produtividade  |
| SQLite Inicial    | Facilidade acadêmica       |
| FBV               | Curva de aprendizado menor |
| Django Admin      | Administração rápida       |

---

# 15. Requisitos Arquiteturais

## A aplicação deverá:

* Utilizar exclusivamente Django como framework principal;
* Utilizar Django REST Framework (DRF) para ingestão de dados;
* Utilizar templates HTML server-side para renderização web;
* Utilizar Bootstrap para estilização;
* Utilizar ORM nativo;
* Utilizar autenticação nativa para o painel web;
* Utilizar autenticação via Token para a API;
* Utilizar Django Admin;
* Consumir dados diretamente do banco (pela view) para a renderização.

---

# 16. Restrições Arquiteturais

## Não utilizar nesta versão

* React;
* Vue;
* Angular;
* Microservices;
* Mensageria;
* Docker obrigatório;
* Arquitetura distribuída.

*Nota: O uso de API REST é restrito apenas à rota de ingestão de dados via DRF. Não construir APIs REST complexas de consulta para SPA/frontend nesta versão.*

---

# 17. Conclusão

A arquitetura do QAgent Analytics foi projetada para priorizar simplicidade, organização e produtividade utilizando recursos nativos do Django.

A solução funcionará como uma camada analítica responsável pela leitura dos dados produzidos pelo QAgent e pela renderização visual dos dashboards de monitoramento e qualidade de software.

A abordagem escolhida reduz complexidade técnica e facilita a implementação acadêmica e manutenção futura do projeto.
