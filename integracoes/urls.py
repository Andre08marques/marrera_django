from django.urls import path
from .views import ixc


urlpatterns = [
    path('ixc/', ixc, name='ixc'),
   
]

