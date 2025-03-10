from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib import messages
from .forms import Instanciaform
from django.contrib.auth.models import User
from main.apps.whatsapp.models import whatsapp, InstanceGroup, Mensagem
from main.src.agents.evolution_agent import Evolution
from main.src.httperro import HttpErrors
import qrcode
from io import BytesIO
from base64 import b64encode


def is_valid_queryparam(param):
    return param != '' and param is not None

@method_decorator(login_required(login_url='login'), name='dispatch')
class Instanceadd(View):

    def get(self, request):
        form = Instanciaform()
        context = {
            "form": form
        }
        return render(request, 'instancia/instancia_add.html', context)
    
    def post(self, request):
        form = Instanciaform(request.POST)
        user = User.objects.get(username=request.user)
        ev = Evolution()
        try:
            instancia = ev.instance_create(request.POST.get("name"))
        except HttpErrors as errors:
            messages.error(request,f'Errou ao tentar criar instância. Erro: {errors} entre em contato com o suporte.')
            return redirect("home") 
        if form.is_valid():
            instance = form.save(commit=False)
            instance.usuario = user
            instance.key = instancia['response']['token']
            instance.status = 'close'
            instance.save()
            return redirect("home") 


@method_decorator(login_required(login_url='login'), name='dispatch')
class InstanceRecreate(View):

    def get(self, request, id):
        instancia = whatsapp.objects.get(pk=id)
        ev = Evolution()
        try:
            instance_desconectar = ev.instance_desconect(instancia.key, instancia.key)
            instance_delete = ev.instance_delete(instancia.key, instancia.key)
            instance_create = ev.instance_recreate(instancia.nome, instancia.key)
            messages.success(request,f'Intancia recriada com sucesso')
            return redirect("home")
        except:
            instance_create = ev.instance_recreate(instancia.nome, instancia.key)
            messages.success(request,f'Intancia recriada com sucesso')
            return redirect('home')
        
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class Instancestatus(View):
    
    def get(self, request, id):
        ev = Evolution()
        instance = whatsapp.objects.get(pk=id)
        response = ev.instance_status(instance.key, instance.key)
        status_code = (response.get('status_code'))
        if ((status_code >= 200) and (status_code <= 299)):
            if response['response']['instance']['state'] == "connecting":
                instance.status = 'connecting'
                instance.save()
                return HttpResponse(f"<span id='instancestatus' style='color: orange;'>Conectando</span>")
            elif response['response']['instance']['state'] == "close":
                instance.status = 'close'
                instance.save()
                return HttpResponse(f"<span id='instancestatus' style='color: red;'>Desconectado</span>")
            else:
                instance.status = 'open'
                instance.save()
                return HttpResponse(f"<span id='instancestatus' style='color: green;'>Conectado</span>")
            
        messages.error(request,f'Houver um erro para obter o status da instância. Se esse erro persistir, entre em contato com o suporte.')
        return redirect('home')

@method_decorator(login_required(login_url='login'), name='dispatch')
class Instanceconect(View):
    
    def get(self, request, id):
        ev = Evolution()
        instance = whatsapp.objects.get(pk=id)
        try:
            instance_conect = ev.instance_connect(instance.key, instance.key)
            code = instance_conect['response']['code']
            qr_code_img = qrcode.make(code)
            buffer = BytesIO()
            qr_code_img.save(buffer)
            buffer.seek(0)
            encoded_img = b64encode(buffer.read()).decode()
            qr_code_data = f'data:image/png;base64,{encoded_img}'
            context = {
                'instanceid': id,
                'qrcode': qr_code_data,
            }
            return render(request, 'instancia/instancia_conect.html',context)
        except HttpErrors as errors:
            messages.error(request,f'Houve um erro ao tentar conectar instância. Erro: {errors} Se esse erro persistir, entre em contato com o suporte.')
            return render(request, 'instancia/instancia_conect.html')

@method_decorator(login_required(login_url='login'), name='dispatch')
class Instancedesconect(View):
    
    def get(self, request, id):
        ev = Evolution()
        instance = whatsapp.objects.get(pk=id)
        try:
            instance_desconect = ev.instance_desconect(instance.key, instance.key)
            return redirect("home")
        except HttpErrors as errors:
            messages.error(request,f'Houve um erro ao tentar desconectar instância. Erro: {errors} Se esse erro persistir, entre em contato com o suporte.')
            return redirect('home')
        
@method_decorator(login_required(login_url='login'), name='dispatch')
class Instancedelete(View):

    def get(self, request, id):
        instancia = whatsapp.objects.get(pk=id)
        ev = Evolution()
        try:
            instance_delete = ev.instance_delete(instancia.key, instancia.key)
            instancia.delete()
            return redirect("home")
        except HttpErrors as errors:
            instancia.delete()
            return redirect('home')


@method_decorator(login_required(login_url='login'), name='dispatch')
class InstanceGroupList(View):

    def get(self, request, id):

        instancegroups = InstanceGroup.objects.all()

        grupo = request.GET.get('grupo')
        filter_query =  Q()
        if is_valid_queryparam(grupo):
            filter_query.add(Q(name__icontains=grupo), Q.AND)
        
        filter_query.add(Q(instance=id), Q.AND)
        
        instancegroups = InstanceGroup.objects.filter(filter_query)

        paginator = Paginator(instancegroups, 15)
        page_number = request.GET.get('page') 
        page_obj = paginator.get_page(page_number) 

        context = {
           'page_title': 'Grupos',
           'page_obj': page_obj,
           'instanceid': id
        }
        
        return render(request, 'group/instancegroup_list.html', context)

class InstanceGroupSync(View):

    def get(self, request, id):

        instance = whatsapp.objects.get(pk=id)
        if instance.status != 'open':
            messages.error(request, "Não foi possível sincronizar os grupos. verifique se sua instância está conectada e tente novmanete.")
            url = reverse("instancegrouplist", args=[id])
            return redirect(url)
        
        ev = Evolution()
        response = ev.instance_get_group(instance.key, instance.key)
        if response['status_code']:
            InstanceGroup.objects.all().delete()
            data =  (response['response'])
            for group in data:

                InstanceGroup.objects.create(name=group['subject'], groupid=group['id'], instance=instance)
            url = reverse("instancegrouplist", args=[id])
            messages.success(request, "Grupos sincronizado com sucesso.")
            return redirect(url)
        
        messages.error(request, "Não foi possível sincronizar os grupos. se esse erro persistir, entre em contato com o suporte.")
        url = reverse("instancegrouplist", args=[id])
        return redirect(url)
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class MsgList(View):

    def get(self, request, id):
        owner = User.objects.get(username=request.user)
        mensagens = Mensagem.objects.filter(owner=owner)

        
        status = request.GET.get('status')
        numero = request.GET.get('numero')
        instance = request.GET.get('instance')

        filter_query =  Q()
        
        
        if is_valid_queryparam(instance):
            filter_query.add(Q(Instance=instance), Q.AND)

        if is_valid_queryparam(status):
            filter_query.add(Q(status=status), Q.AND)

        if is_valid_queryparam(numero):
            filter_query.add(Q(numero__icontains=numero), Q.AND)
        
        filter_query.add(Q(owner=owner), Q.AND)
        
        mensagens = Mensagem.objects.filter(filter_query)


        paginator = Paginator(mensagens, 15)
        page_number = request.GET.get('page') 
        page_obj = paginator.get_page(page_number) 

        context = {
            "page_title": "Mensagens enviadas",
            "page_obj": page_obj
        }

        return render(request, 'mensagens/mensagens.html', context)
