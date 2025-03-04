from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import views, response, status
from django.contrib.auth.models import User
from main.apps.externaluser.models import Fatura_gerada
from main.apps.whatsapp.models import whatsapp
from .tasks import send_menssage
import json


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



@method_decorator(csrf_exempt, name='dispatch')
class CobreFacilWebhookView(APIView):
    """
    View para receber o webhook do Cobre Facil e atualizar o status do pagamento.
    """

    def get(self, request):
        return JsonResponse({"error": "Método não permitido"}, status=405)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            id_fatura = data.get("id")  
            status = data.get("status")

          
            fatura = Fatura_gerada.objects.filter(id_fatura=id_fatura).first()
            if fatura and status == "paid":
                fatura.status_fatura = "pago"
                fatura.updated_at = now()
                fatura.save()

              
                if fatura.cliente:
                    fatura.cliente.adicionar_mes()

                return JsonResponse({"message": "Pagamento confirmado e vencimento atualizado"}, status=200)

            return JsonResponse({"error": "Fatura não encontrada ou status inválido"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        
        