from django.shortcuts import render
from externaluser.models import perfil
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import auth,messages
from externaluser.forms import PerfilForm
from django.contrib.auth.models import User
from whatsapp.models import whatsapp
from .forms import WhatsappForm
import qrcode
from io import BytesIO
from base64 import b64encode
from .functions import create_instance,get_instances, instance_connect, instance_desconect,instance_delete

# Create your views here.
@login_required
def home(request):
    whatsapp_total = whatsapp.objects.filter(usuario=request.user).count()
    whatsapp_ativo = whatsapp.objects.filter(usuario=request.user,status="open").count()
    whatsapp_inativo = whatsapp.objects.filter(usuario=request.user,status="close").count()
    whatsapp_context = { 

                "whatsapp_total": whatsapp_total,
                "whatsapp_ativo": whatsapp_ativo,
                "whatsapp_inativo": whatsapp_inativo,                     
    }
    zap = whatsapp.objects.filter(usuario=request.user)
    cliente = perfil.objects.filter(usuario=request.user)
    return render(request, 'hod_template/hod_content.html',{'whatsapp_context': whatsapp_context, 'zap': zap, cliente: 'cliente'})

@login_required
def listar_perfil(request):
    pesquisa = request.GET.get('pesquisa', None)
    if pesquisa:
       profile = perfil.objects.filter(nome=pesquisa) 
       profile_paginator = Paginator(profile, 10)
       page_num = request.GET.get('page', None)
       page = profile_paginator.get_page(page_num)
       context = {
            'page': page,
            'page_title': 'Gerenciar Instâncias'
        }
    else:
       profile = perfil.objects.all().order_by("id")
       profile_paginator = Paginator(profile, 10)
       page_num = request.GET.get('page')
       page = profile_paginator.get_page(page_num)
       context = {
            'page': page,
            'page_title': 'Gerenciar Perfis'
        }
    return render(request, 'perfil/perfil_listar.html', context)
   

@login_required
def editar_perfil(request, id):
    profile = get_object_or_404(perfil, pk=id)
    form = PerfilForm(request.POST or None, request.FILES or None, instance=profile)
    context = {
        'form': form,
        'page_title': 'Edit perfil'
    }
    if form.is_valid():
        form.save()
        messages.success(request,'perfil atualizado com sucesso')
        return redirect('listarperfil')
    return render(request, 'perfil/perfil_editar.html', context)

@login_required
def perfil_delete(request, id):
    profile = perfil.objects.filter(pk=id).values('usuario__id')
    usuario = User.objects.get(pk=profile[0]['usuario__id'])
    usuario.delete()
    return redirect('listarperfil')


@login_required
def reset_password(request):
    id_perfil = request.POST['id']
    id = perfil.objects.filter(pk=id_perfil).values('usuario__id')
    usuario = User.objects.get(pk=id[0]['usuario__id'])
    new_password = request.POST["senha"]
    usuario.set_password(new_password)
    usuario.save()
    messages.success(request, 'A senha foi alterada com sucesso')
    return redirect("listarperfil")

#Instâncias
@login_required
def whatsapp_list(request):
    pesquisa = request.GET.get('pesquisa', None)
    if pesquisa:
       zap = whatsapp.objects.filter(nome=pesquisa) 
       zap_paginator = Paginator(zap, 10)
       page_num = request.GET.get('page', None)
       page = zap_paginator.get_page(page_num)
       context = {
            'page': page,
            'page_title': 'Gerenciar Instâncias'
        }
    else:
       zap = whatsapp.objects.all()
       zap_paginator = Paginator(zap, 10)
       page_num = request.GET.get('page')
       page = zap_paginator.get_page(page_num)
       context = {
            'page': page,
            'page_title': 'Gerenciar Instâncias'
        }
    return render(request, 'zap/whatsapplist.html', context)

@login_required
def whatsapp_form(request):
    usuario = request.user
    if request.method == "GET":
        form = WhatsappForm()
        context = {
            'form': form,
            'page_title': 'Adicionar Instâncias'
        }
        return render(request, 'zap/whatsappform.html', context=context)
    else:
        qtd_instancia = whatsapp.objects.filter(usuario=request.user).count()
        qtd_plano = perfil.objects.filter(usuario=request.user).values('plano__quantidade')
        if qtd_instancia >= qtd_plano[0]['plano__quantidade']:
            messages.error(request,'Você atingiu o número máximo de instâncias que o seu plano permite! Entre em contato com o suporte para saber mais')
            return redirect('home')
        else:
            instancia = create_instance()
            form = WhatsappForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.usuario = usuario
                instance.key = instancia["hash"]['apikey']
                instance.save()
                client = form.save()
                messages.success(request,'Instância Cadastrada com sucesso')
                return redirect('whatsapp_list')

@login_required
def conectar(request, id):
    zapp = whatsapp.objects.filter(pk=id).values('key','nome')
    apikey = (zapp[0]['key'])
    nome = (zapp[0]['key'])
    sapqrcode = instance_connect(apikey,nome)
    code = sapqrcode['code']
    qr_code_img = qrcode.make(code)
    buffer = BytesIO()
    qr_code_img.save(buffer)
    buffer.seek(0)
    encoded_img = b64encode(buffer.read()).decode()
    qr_code_data = f'data:image/png;base64,{encoded_img}'
    zap = whatsapp.objects.all()
    zap_paginator = Paginator(zap, 10)
    page_num = request.GET.get('page')
    page = zap_paginator.get_page(page_num)
    context = {
        'page': page,
        'qrcode': qr_code_data,
        'page_title': 'Gerenciar Instâncias'
    }
    return render(request, 'zap/whatsapplist.html',context)

@login_required
def whatsapp_desconect(request, id):
    zapp = whatsapp.objects.filter(pk=id).values('key','nome')
    apikey = (zapp[0]['key'])
    nome = (zapp[0]['nome'])
    data = instance_desconect(apikey,nome)
    zapp = whatsapp.objects.filter(usuario=request.user)
    zapp_paginator = Paginator(zapp, 10)
    page_num = request.GET.get('page')
    page = zapp_paginator.get_page(page_num)
    context = {
        'page': page,
        'page_title': 'Gerenciar Instâncias'
    }
    return redirect('whatsapp_list')

@login_required
def whatsapp_delete(request, id):
    zapp = whatsapp.objects.filter(pk=id).values('key')
    apikey = (zapp[0]['key'])
    nome = (zapp[0]['key'])
    data = instance_delete(apikey,nome)
    instancia = get_object_or_404(whatsapp, pk=id)
    dados = instancia.delete()
    print (request.GET)
    return redirect('whatsapp_list')