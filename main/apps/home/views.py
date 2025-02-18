from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from main.apps.whatsapp.models import whatsapp
from main.apps.externaluser.models import perfil


@method_decorator(login_required(login_url='login'), name='dispatch')
class Home(View):

    def get(self, request):
        whatsapp_total = whatsapp.objects.filter(usuario=request.user).count()
        whatsapp_ativo = whatsapp.objects.filter(usuario=request.user,status="open").count()
        whatsapp_inativo = whatsapp.objects.filter(usuario=request.user,status="close").count()
        zap = whatsapp.objects.filter(usuario=request.user)
        cliente = perfil.objects.get(usuario=request.user)
        whatsapp_context = { 

                    "whatsapp_total": whatsapp_total,
                    "whatsapp_ativo": whatsapp_ativo,
                    "whatsapp_inativo": whatsapp_inativo,  
                    "cliente": cliente,
                    "zap": zap                  
        }
        return render(request, 'hod_template/hod_content.html',whatsapp_context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class UserChangePassword(View):
    def get(self, request):
        perfil = User.objects.get(username=request.user)
        context = {
            'page_title': 'Reset Password',
            'perfil': perfil
        }
        return render(request, 'userchangepassword.html', context)
    
    def post(self, request):

        new_password = request.POST["senha"]
        user = User.objects.get(username=request.user)
        user.set_password(new_password)
        user.save()
        messages.success(request,'Senha alterada com sucesso')
        return redirect('home')

    