from django.contrib import admin
from .models import perfil, Plano, Fatura_gerada

# Register your models here.

admin.site.register(perfil)
admin.site.register(Plano)
admin.site.register(Fatura_gerada)

