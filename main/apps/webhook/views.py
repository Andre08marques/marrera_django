from django.shortcuts import render
from django.shortcuts import render, HttpResponse
from rest_framework import views, response, status
from django.contrib.auth.models import User
from main.apps.whatsapp.models import whatsapp
from .tasks import send_menssage


class webhookSendMsgSgpView(views.APIView):
    
    def get(self, request):
        instance = request.GET.get('instancia')
        key = request.GET.get('key')
        to = request.GET.get('to'),
        msg = request.GET.get('msg')
        try:
            instance_get = whatsapp.objects.get(nome=instance)
            send_menssage.delay(instance,key,to,msg)
            return HttpResponse("Mensagem na fila para ser enviada.")
        except whatsapp.DoesNotExist:
            return HttpResponse("Não foi possível enviar a mensagem, verifique se o nome da instância está correto na configuração do sgp")