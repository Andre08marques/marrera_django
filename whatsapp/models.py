from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class whatsapp(models.Model):
    nome = models.CharField(max_length=60)
    key = models.CharField(max_length=60)
    status = models.CharField(max_length=60, default="desconectado")
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    def __str__(self):
        return self.nome