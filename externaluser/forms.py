from django import forms
from django.forms.widgets import DateInput, TextInput
from .models import perfil

#
class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

class PerfilForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(PerfilForm, self).__init__(*args, **kwargs)

    class Meta:
        model = perfil
        fields = ['email','cpf_cnpj','cpf_or_cnpj','celular','nome','plano','descricaoEndereco','cep','numero','complemento','bairro','cidade','estado']
        widgets = {
            "celular": forms.TextInput(attrs={'class':'form-control custom-input phone-mask'}),
            "cep": forms.TextInput(attrs={'class':'form-control custom-input'}),
            "checkbox": forms.TextInput(attrs={'type':'checkbox'})
        }