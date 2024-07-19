from django.urls import path
from .views import ixc, sistemas


urlpatterns = [
    path('ixc/', ixc, name='ixc'),
    path('sistemas/', sistemas, name='integracoes')
   
]

