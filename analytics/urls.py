from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import api

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('execucoes/', views.lista_execucoes, name='lista_execucoes'),
    path('execucoes/<int:id>/', views.detalhe_execucao, name='detalhe_execucao'),
    
    # API REST
    path('api/v1/execucoes/', api.ExecucaoTesteViewSet.as_view({'post': 'create'}), name='api_create_execucao'),
]
