from django.contrib import admin
from .models import whatsapp

class Whatsappadmin(admin.ModelAdmin):
    list_display = ('nome', 'key', 'status', 'usuario')
    list_filter = ('course', 'student')
    search_fields = ('lasson',)

admin.site.register(whatsapp,Whatsappadmin)

