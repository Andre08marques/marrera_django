from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
tipo_pessoa = (
    ("1", "CPF"),
    ("2", "CNPJ")
)

status = (
    ("1", "ATIVO"),
    ("2", "INATIVO")
)

estado = (
            ("AC", "Acre"),
            ("AL", "Alagoas"),
            ("AP", "Amapá"),
            ("AM", "Amazonas"),
            ("BA", "Bahia"),
            ("CE", "Ceará"),
            ("DF", "Distrito Federal"),
            ("ES", "Espírito Santo"),
            ("GO", "Goiás"),
            ("MA", "Maranhão"),
            ("MT", "Mato Grosso"),
            ("MS", "Mato Grosso do Sul"),
            ("MG", "Minas Gerais"),
            ("PA", "Pará"),
            ("PB", "Paraíba"),
            ("PR", "Paraná"),
            ("PE", "Pernambuco"),
            ("PI", "Piauí"),
            ("RJ", "Rio de Janeiro"),
            ("RN", "Rio Grande do Norte"),
            ("RS", "Rio Grande do Sul"),
            ("RO", "Rondônia"),
            ("RR", "Roraima"),
            ("SC", "Santa Catarina"),
            ("SP", "São Paulo"),
            ("SE", "Sergipe"),
            ("TO", "Tocantins")
)

def tree_day_hence():
    return timezone.now() + timezone.timedelta(days=3)

class Plano(models.Model):
    plano = models.CharField(max_length=40, null=True)
    price = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    status = models.CharField(choices=status, max_length=40, null=True)
    def __str__(self):
        return self.plano
    
class perfil(models.Model):
    nome = models.CharField(max_length=50, null=True)
    cpf_cnpj = models.CharField(choices=tipo_pessoa, max_length=20, null=True)
    cpf_or_cnpj = models.CharField(max_length=30, unique=True, null=True )
    plano = models.ForeignKey(Plano, blank=True, null=True, on_delete=models.PROTECT)
    celular = models.CharField(max_length=15, unique=True, null=True )
    email = models.CharField(max_length=50, null=True)
    descricaoEndereco = models.CharField(max_length=100, null=True)
    cep  = models.CharField(max_length=15, null=True )
    numero = models.IntegerField(null=True )
    complemento = models.CharField(max_length=100, null=True)
    bairro = models.CharField(max_length=50, null=True)
    cidade = models.CharField(max_length=50, null=True)
    estado = models.CharField(choices=estado, max_length=50, null=True)
    usuario = models.OneToOneField(User, blank=True, null=True, on_delete=models.PROTECT)
    cobrefacil_id = models.CharField(max_length=50, null=True)
    vencimento = models.DateField(default=tree_day_hence)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.nome

class Fatura_gerada(models.Model):
    cliente = models.ForeignKey(perfil, related_name='perfil', null=True, on_delete=models.SET_NULL)
    id_fatura = models.CharField(max_length=50, null=True)
    payable_with = models.CharField(max_length=50, null=True)
    due_date = models.CharField(max_length=50, null=True)
    price = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    status_fatura = models.CharField(max_length=50, default="processing", null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.id_fatura



