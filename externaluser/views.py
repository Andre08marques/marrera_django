from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import auth,messages
from .forms import PerfilForm
from django.contrib.auth.models import User
from .models import perfil, Fatura_gerada
from .functions import cadastrar_cliente, autenticar, gerar_faturar
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import date

import json
# Create your views here.

#ge
def thirty_day_hence(data):
    return data + timezone.timedelta(days=30)

# Create your views here.
def register(request):
    form = PerfilForm()
    if request.method == "POST":
        form = PerfilForm(request.POST)
        if form.is_valid():
            username = (request.POST["email"])
            email =  (request.POST["email"])
            senha =  (request.POST["senha"])
            print ()
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

def gerar_fatura(request):
    p = perfil.objects.filter(email=request.user).values('cobrefacil_id','vencimento','plano__price')
    token = autenticar()
    price = (p[0]['plano__price'])
    vencimento = (p[0]['vencimento'])
    cobrefacilid = (p[0]['cobrefacil_id'])
    data = gerar_faturar(token,cobrefacilid,vencimento,price)
    if data['success'] == True:
        fatura_id = data['data']['id']
        cliente = perfil.objects.get(email=request.user) 
        print (cliente)
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
               novo_vencimento = thirty_day_hence(timezone.now())
               p = perfil.objects.filter(cobrefacil_id=data_dict['data']['customer']['id']).update(vencimento=novo_vencimento)
           else:
               novo_vencimento = thirty_day_hence(vencimento[0]['cliente__vencimento'])
               p = perfil.objects.filter(cobrefacil_id=data_dict['data']['customer']['id']).update(vencimento=novo_vencimento)

        return HttpResponse("Webhook received!")
        

    
