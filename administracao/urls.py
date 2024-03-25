from django.urls import path
from .views import listar_perfil, editar_perfil, reset_password,perfil_delete,whatsapp_list, whatsapp_form,conectar,whatsapp_desconect,whatsapp_delete

urlpatterns = [
    path('listarperfil/', listar_perfil, name='listarperfil'),
    path('editarperfil/<int:id>', editar_perfil, name='editarperfil'),
    path('deleteperfil/<int:id>', perfil_delete, name='deleteperfil'),
    path('resetpassword/', reset_password, name='resetpassword'),
    # trabalhar com instancias
    path('whatsapplist/', whatsapp_list, name='whatsapp_list'),
    path('whatsappform/', whatsapp_form, name='whatsapp_form'),
    # conecta com a api do whatsapp
    path('conectar/<int:id>', conectar, name='conectar'),
    # desconectar com a api do whatsapp
    path('whatsapp_desconect/<int:id>', whatsapp_desconect, name='whatsapp_desconect'),
    # deletar com a api do whatsapp
    path('whatsapp_delete/<int:id>', whatsapp_delete, name='whatsapp_delete')
    
]