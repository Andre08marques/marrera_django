from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import auth,messages
from .forms import WhatsappForm
from .models import whatsapp
from externaluser.models import perfil
from .functions import create_instance,get_instances, instance_connect, instance_desconect,instance_delete
import qrcode
from io import BytesIO
from base64 import b64encode

# Create your views here.
@login_required
def home(request):
    instancias = get_instances()
    if instancias != "timeout": 
        
        for instance in instancias:
            instan = instance['instance']['instanceName']
            status = instance['instance']['status']
            whatsapp.objects.filter(key=instan).update(status=status)
        whatsapp_total = whatsapp.objects.filter(usuario=request.user).count()
        whatsapp_ativo = whatsapp.objects.filter(usuario=request.user,status="open").count()
        whatsapp_inativo = whatsapp.objects.filter(usuario=request.user,status="close").count()
        whatsapp_context = { 

                    "whatsapp_total": whatsapp_total,
                    "whatsapp_ativo": whatsapp_ativo,
                    "whatsapp_inativo": whatsapp_inativo,                     
        }
        zap = whatsapp.objects.filter(usuario=request.user)
        cliente = perfil.objects.filter(usuario=request.user).values("plano__plano","vencimento")
        print (cliente)
        cliente_ok = (cliente[0])
        return render(request, 'hod_template/hod_content.html',{'whatsapp_context': whatsapp_context, 'zap': zap, "cliente": cliente_ok})
    else:
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
        print (cliente)
        return render(request, 'hod_template/hod_content.html',{'whatsapp_context': whatsapp_context, 'zap': zap, cliente: 'cliente'})

@login_required
def whatsapp_list(request):
    instancias = get_instances()
    for instance in instancias:
        instan = instance['instance']['instanceName']
        status = instance['instance']['status']
        whatsapp.objects.filter(nome=instan).update(status=status)
    pesquisa = request.GET.get('pesquisa', None)
    if pesquisa:
       zap = whatsapp.objects.filter(usuario=request.user, nome=pesquisa) 
       zap_paginator = Paginator(zap, 10)
       page_num = request.GET.get('page', None)
       page = zap_paginator.get_page(page_num)
       context = {
            'page': page,
            'page_title': 'Gerenciar Instâncias'
        }
    else:
       zap = whatsapp.objects.filter(usuario=request.user)
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
                return redirect('home')

      


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
    zap = whatsapp.objects.filter(usuario=request.user)
    # context
    whatsapp_total = whatsapp.objects.filter(usuario=request.user).count()
    whatsapp_ativo = whatsapp.objects.filter(usuario=request.user,status="open").count()
    whatsapp_inativo = whatsapp.objects.filter(usuario=request.user,status="close").count()
    whatsapp_context = { 

                "whatsapp_total": whatsapp_total,
                "whatsapp_ativo": whatsapp_ativo,
                "whatsapp_inativo": whatsapp_inativo, 
                'qrcode':     qr_code_data                   
    }
    return render(request, 'hod_template/hod_content.html',{'whatsapp_context': whatsapp_context, 'zap': zap})

# Create your views here.
@login_required
def whatsapp_desconect(request, id):
    zapp = whatsapp.objects.filter(pk=id).values('key','nome')
    apikey = (zapp[0]['key'])
    nome = (zapp[0]['nome'])
    data = instance_desconect(apikey,nome)
    print (data)
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
    return redirect('home')
