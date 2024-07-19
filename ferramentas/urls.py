from django.urls import path
from .views import listar_grupos

urlpatterns = [
    path('listargrupos/', listar_grupos, name='listargrupos'),
]