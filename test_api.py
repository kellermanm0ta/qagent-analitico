import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import Client

# Ensure user exists
user, created = User.objects.get_or_create(username='admin_test')
if created:
    user.set_password('admin123')
    user.save()

# Create or get token
token, _ = Token.objects.get_or_create(user=user)
print(f"Token: {token.key}")

# Use the test client to simulate a POST request
client = Client()

payload = {
    "data_execucao": "2026-05-31T14:00:00Z",
    "total_testes": 10,
    "testes_sucesso": 8,
    "testes_falha": 2,
    "tempo_execucao": 1.5,
    "cobertura_codigo": 85.5,
    "status": "FALHA",
    "logs": [
        {
            "arquivo": "test_auth.py",
            "mensagem": "AssertionError: expected True but got False"
        },
        {
            "arquivo": "test_views.py",
            "mensagem": "404 Not Found"
        }
    ]
}

response = client.post(
    '/api/v1/execucoes/', 
    payload, 
    content_type='application/json',
    HTTP_AUTHORIZATION=f'Token {token.key}'
)

print(f"Status Code: {response.status_code}")
if response.status_code == 201:
    print("Success! Data created:")
    print(response.json())
else:
    print("Error:")
    print(response.json())
