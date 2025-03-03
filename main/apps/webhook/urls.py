from django.urls import path
from . import views

urlpatterns = [

    path('webhook/sgp/msg', views.webhookSendMsgSgpView.as_view(), name='sgpsendmsg')
]