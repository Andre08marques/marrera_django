from django.urls import path
from .views import register, gerar_fatura, reset_password, webhook, whatsapp_form,conectar,whatsapp_desconect,whatsapp_delete,whatsapp_sync


urlpatterns = [
    path('register/', register, name='register'),
    path('fatura/', gerar_fatura, name='fatura'),
    path('reset_password/', reset_password, name='reset_password'),
    path('webhook/', webhook, name='webhook'),
    # criar instâncias 
    path ('externaluser_criar',whatsapp_form, name='externaluser_criar' ),
    # conecta com a api do whatsapp
    path('conectar/<int:id>', conectar, name='externaluser_conectar'),
    # desconectar com a api do whatsapp
    path('whatsapp_desconect/<int:id>', whatsapp_desconect, name='externaluser_whatsapp_desconect'),
    # deletar com a api do whatsapp
    path('whatsapp_delete/<int:id>', whatsapp_delete, name='externaluser_whatsapp_delete'),
    # syncroniza instance
    path('whatsapp_sync/<int:id>', whatsapp_sync, name='whatsapp_sync')
]