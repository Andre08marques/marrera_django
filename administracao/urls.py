from django.urls import path
from .views import listar_perfil, editar_perfil, reset_password,perfil_delete

urlpatterns = [
    path('listarperfil/', listar_perfil, name='listarperfil'),
    path('editarperfil/<int:id>', editar_perfil, name='editarperfil'),
    path('deleteperfil/<int:id>', perfil_delete, name='deleteperfil'),
    path('resetpassword/', reset_password, name='resetpassword'),
]