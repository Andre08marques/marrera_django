from celery import shared_task
from django.conf import settings
from main.apps.whatsapp.models import whatsapp, Mensagem
from ...src.agents.evolution_agent import Evolution 
from main.src.httperro import HttpErrors
import time

@shared_task(name="send_msg_text")
def send_menssage(instance,key,to,msg):
    ev = Evolution()
    instance_obj = whatsapp.objects.get(nome=instance)
    text = msg.replace('|', ' ')
    msg_list = msg.split('|')
    time.sleep(int(settings.SLEEPMSG))
    try:
        for m in msg_list:
            response = ev.instance_send_text(key,key,to,m)
            time.sleep(1)
       
     
        Mensagem.objects.create(
                                Instance=instance,
                                status="1",
                                owner=instance_obj.usuario,
                                numero=to,
                                log="Mensagem Enviada"
                                )
        

    except HttpErrors as errors:
        Mensagem.objects.create(
                                Instance=instance, 
                                status="2",
                                owner=instance_obj.usuario,
                                numero=to,
                                log=errors
                                )
     