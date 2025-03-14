from django import forms
from django.forms.widgets import DateInput, TextInput
from .models import whatsapp

class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

class WhatsappForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(WhatsappForm, self).__init__(*args, **kwargs)

    class Meta:
        model = whatsapp
        fields = ['nome']
    
            
class Instanciaform(FormSettings):
    def __init__(self, *args, **kwargs):
        super(Instanciaform, self).__init__(*args, **kwargs)

    class Meta:
        model = whatsapp
        fields = ["nome"]
        labels = {
           "nome": "Nome*",

        }