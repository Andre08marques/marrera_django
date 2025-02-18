from django.urls import path
from .views import UserChangePassword


urlpatterns = [
    path('changepassword',UserChangePassword.as_view(), name='userchangepassword')
]