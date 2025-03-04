from django.urls import path
from . import views

urlpatterns = [

    path('webhook/sgp/msg', views.webhookSendMsgSgpView.as_view(), name='sgpsendmsg'),
    path('webhook/cobrefacil/pay', views.CobreFacilWebhookView.as_view(), name='cobrefacilreceberpagamentos'),
    
]