from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery('main')
app.conf.enable_utc = False

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'Mudando status da instancia': {
        'task': 'check_instance_status',
        'schedule': 59.0,
        'options': {'queue': 'check_instance_status'}
    },
}