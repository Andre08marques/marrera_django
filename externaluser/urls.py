from django.urls import path
from .views import register, gerar_fatura, reset_password, webhook

urlpatterns = [
    path('register/', register, name='register'),
    path('fatura/', gerar_fatura, name='fatura'),
    path('reset_password/', reset_password, name='reset_password'),
    path('webhook/', webhook, name='webhook')
]