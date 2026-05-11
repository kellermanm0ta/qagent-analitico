# QAgent Analytics

O **QAgent Analytics** é uma aplicação web focada no monitoramento e visualização analítica dos testes e métricas de qualidade gerados pelo QAgent. Este sistema fornece um dashboard intuitivo, lista detalhada de execuções e análise minuciosa de logs de erros, tudo empacotado em uma interface web moderna baseada em Django e Bootstrap 5 (Dark Mode & Glassmorphism).

## 🚀 Tecnologias e Versões Requeridas

*   **Linguagem Principal:** Python 3.12+
*   **Framework Web:** Django 5.0+
*   **Banco de Dados (Desenvolvimento):** SQLite
*   **Frontend:** HTML5, CSS3, Bootstrap 5.3+

## 💻 Como Iniciar em Ambiente de Desenvolvimento

Siga os passos abaixo para configurar e rodar o projeto na sua máquina local.

### 1. Preparação do Ambiente Virtual

É recomendado utilizar um ambiente virtual para isolar as dependências do projeto. Crie e ative o ambiente virtual **dentro do diretório raiz do projeto** (`qagent-analitico`):

**No Linux/macOS:**
```bash
# Crie o ambiente virtual
python3 -m venv .venv

# Ative o ambiente
source .venv/bin/activate
```

**No Windows:**
```cmd
# Crie o ambiente virtual
python -m venv .venv

# Ative o ambiente
.venv\Scripts\activate
```

### 2. Instalação das Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias listadas no `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Configuração do Banco de Dados

Aplique as migrações para criar as tabelas do banco de dados SQLite:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Populando o Banco com Dados Iniciais (Opcional, mas Recomendado)

O projeto conta com um script `seed.py` que cria o superusuário padrão e insere algumas execuções falsas para que o dashboard não fique vazio. Para executá-lo:

```bash
python seed.py
```

Isso criará o acesso de administrador:
*   **Usuário:** `admin`
*   **Senha:** `admin`

### 5. Executando o Servidor de Desenvolvimento

Agora você pode iniciar o servidor local do Django:

```bash
python manage.py runserver
```

Acesse a aplicação no seu navegador através do endereço:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

Você também pode acessar o painel administrativo nativo do Django para gerenciar os dados em:
👉 **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)**

## 📂 Estrutura do Projeto

*   `analytics/`: Aplicação principal do Django (Models, Views, URLs).
*   `config/`: Configurações principais do projeto Django (`settings.py`, `urls.py`).
*   `templates/`: Componentes visuais HTML utilizando Bootstrap 5.
    *   `dashboard/`: Telas e visões analíticas.
    *   `base.html`: Layout mestre.
    *   `login.html`: Tela de autenticação.
*   `seed.py`: Script para popular dados iniciais.
