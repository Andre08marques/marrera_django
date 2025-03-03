from django.contrib import admin
from .models import whatsapp, Mensagem

class Whatsappadmin(admin.ModelAdmin):
    list_display = ('nome', 'key', 'status', 'usuario')
    list_filter = ('nome', 'usuario')
    search_fields = ('usuario',)

admin.site.register(whatsapp,Whatsappadmin)
admin.site.register(Mensagem)

