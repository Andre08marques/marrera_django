from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import Now
from datetime import datetime
from .models import whatsapp
from .functions import get_instances

@shared_task(name="check_instance_status")
def check_instance_status():
    data = get_instances()
    if data != "Error":
        for instance in (data):
            nome = (instance['instance']['instanceName'])
            status = (instance['instance']['status'])
            #print (nome+" "+status)
            zap = whatsapp.objects.filter(key=nome).update(status=status)
            print (zap)
    else:
        print ("Task não realizada")
    