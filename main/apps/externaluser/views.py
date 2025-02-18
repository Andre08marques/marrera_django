from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth,messages
from .forms import PerfilForm
from main.apps.administracao.forms import WhatsappForm
from django.contrib.auth.models import User
from main.apps.whatsapp.models import whatsapp
from .models import perfil, Fatura_gerada
from .functions import cadastrar_cliente, autenticar, gerar_faturar
from main.apps.administracao.functions import create_instance, instance_connect, instance_desconect, instance_delete,sync_instance
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import date
import qrcode
from io import BytesIO
from base64 import b64encode

import json
# Create your views here.

#ge
def thirty_day_hence(data):
    return data + timezone.timedelta(days=30)

def one_day_hence(data):
    return data + timezone.timedelta(days=1)

# Create your views here.
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
    zapp = whatsapp.objects.filter(pk=id).update(status="Connecting")
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

@login_required
def whatsapp_desconect(request, id):
    zapp = whatsapp.objects.filter(pk=id).values('key','nome')
    apikey = (zapp[0]['key'])
    nome = (zapp[0]['key'])
    data = instance_desconect(apikey,nome)
    print (data)
    return redirect('home')

@login_required
def whatsapp_delete(request, id):
    zapp = whatsapp.objects.filter(pk=id).values('key')
    apikey = (zapp[0]['key'])
    nome = (zapp[0]['key'])
    data = instance_delete(apikey,nome)
    instancia = get_object_or_404(whatsapp, pk=id)
    dados = instancia.delete()
    print (request.GET)
    return redirect('home')

@login_required
def whatsapp_sync(request, id):
    zapp = whatsapp.objects.get(pk=id)
    apikey = (zapp.key)
    nome = (zapp.nome)
    data = instance_delete(apikey,nome)
    sync_instance(apikey)
    zapp.status = "close"
    zapp.save()
    return redirect('home')

def register(request):
    form = PerfilForm()
    if request.method == "POST":
        form = PerfilForm(request.POST)
        if form.is_valid():
            username = (request.POST["email"])
            email =  (request.POST["email"])
            senha =  (request.POST["senha"])
            #Adicionar um usuário
            try: 
                user = User.objects.get(username=username)
                messages.error(request, f'Já existe um usuário com este email: {email}')
            except User.DoesNotExist:
                token = autenticar()
                data = cadastrar_cliente(request.POST, token)
                cobrefacil_id =  (data['data']['id'])
                user = User.objects.create_user(f'{username}', f'{email}', f'{senha}')
                user.save()
                
                perfil = form.save(commit=False)
                plano = request.POST['plano']

                perfil.usuario = (user)
                perfil.cobrefacil_id = (cobrefacil_id)
                perfil.save()
                messages.success(request, 'Registrado. Agora faça o login para começar!')
                return redirect('login')
        else:
            messages.success(request, 'algo deu errado')
            
    return render(request, "registration/cadastro.html",{"form": form})
@login_required
def gerar_fatura(request):
    p = perfil.objects.filter(email=request.user).values('cobrefacil_id','vencimento','plano__price')
    token = autenticar()
    price = (p[0]['plano__price'])
    vencimento = one_day_hence(timezone.now())
    cobrefacilid = (p[0]['cobrefacil_id'])
    data = gerar_faturar(token,cobrefacilid,vencimento,price)
    print (data)
    if data['success'] == True:
        fatura_id = data['data']['id']
        cliente = perfil.objects.get(email=request.user) 
        fatura_create = Fatura_gerada.objects.create(cliente=cliente,id_fatura=data['data']['id'], due_date=data['data']['due_date'], price= data['data']['price'])
        return redirect(f'https://app.cobrefacil.com.br/minha-fatura/{fatura_id}')
    else:
        messages.error(request, 'algo deu errado tente mais vez! caso não consiga, entre em contato com o suporte.')
        return redirect('home')
    
@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        data = request.body
        data_dict = json.loads(data.decode("utf-8")) 
        if data_dict['event'] == "invoice.paid":
           vencimento = Fatura_gerada.objects.filter(id_fatura=data_dict['data']['id']).values("cliente__vencimento")
           obj = Fatura_gerada.objects.filter(id_fatura=data_dict['data']['id']).update(status_fatura=data_dict['data']["status"], 
                                                                                        payable_with=data_dict['data']["payment_method"],
                                                                                        price=data_dict['data']["total_paid"],

                                                                                      )
           
           if vencimento[0]['cliente__vencimento'] < date.today():
               novo_vencimento = thirty_day_hence(date.today())
               p = perfil.objects.filter(cobrefacil_id=data_dict['data']['customer']['id']).update(vencimento=novo_vencimento)
           else:
               novo_vencimento = thirty_day_hence(vencimento[0]['cliente__vencimento'])
               p = perfil.objects.filter(cobrefacil_id=data_dict['data']['customer']['id']).update(vencimento=novo_vencimento)

        return HttpResponse("Webhook received!")
    else:
        return HttpResponse("Webhook received!")

# view para trocar a senha do usuário
@login_required
def reset_password(request):
    usuario = User.objects.get(username=request.user)
    new_password = request.POST["senha"]
    usuario.set_password(new_password)
    usuario.save()
    messages.success(request, 'Sua senha foi alterada! Entre com a nova senha')
    return redirect("login")
        

    
