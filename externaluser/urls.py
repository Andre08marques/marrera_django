from django.urls import path
from .views import register, gerar_fatura, webhook

urlpatterns = [
    path('register/', register, name='register'),
    path('fatura/', gerar_fatura, name='fatura'),
    path('webhook/', webhook, name='webhook')
]