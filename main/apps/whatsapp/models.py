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
    

class InstanceGroup(models.Model):
    name = models.CharField(max_length=99)
    groupid = models.CharField(max_length=99)
    instance = models.ForeignKey(whatsapp, related_name="instancegroup", on_delete=models.CASCADE, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


status = (
    ("1", "Mensagem enviada"),
    ("2", "Mensagem não enviada")
)
class Mensagem(models.Model):

    Instance = models.CharField(max_length=99)
    numero = models.CharField(max_length=30, null=True)
    status = models.CharField(max_length=100, choices=status)
    owner = models.ForeignKey(User, related_name="msginstances", on_delete=models.CASCADE, blank=True, null=True)
    mensagem = models.TextField(null=True)
    log = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Instance