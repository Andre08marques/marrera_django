from django.shortcuts import render, redirect
from whatsapp.models import whatsapp
from .functions import get_all_grupos
from django.contrib import auth,messages

# Create your views here.

def listar_grupos(request):
    if request.method == "GET":
        zap = whatsapp.objects.filter(usuario=request.user).values('nome')
        context = {
                'page_title': 'Listar grupos',
                'zap': zap
            }
        return render(request, "listargrupos.html", context)
    else:
        zap = whatsapp.objects.filter(usuario=request.user).values('nome')
        context = {
                'page_title': 'Listar grupos',
                'zap': zap
            }
        instancia = (request.POST['pesquisa'])
        get_key = whatsapp.objects.filter(nome=instancia).values('key')
        key = get_key[0]['key']
        grupos = (get_all_grupos(key))
        grupos_atualizado = []
        for grupo in grupos:
           grupos_atualizado.append({"id": grupo['id'].replace("@g.us", ""),"subject": grupo['subject']})
        if 404 in grupos:
          context = {
                'page_title': 'Listar grupos',
                'zap': zap,
                'grupos': grupos_atualizado
            }
          messages.error(request, 'Desculpe! não conseguimos obter seus grupos. Possíveis problemas \n\n *A instância selecionada não está conectada\n *Aconteceu um erro de comunicação com o servidor.')
          return render(request, "listargrupos.html", context)
        else:
          context = {
                'page_title': 'Listar grupos',
                'zap': zap,
                'grupos': grupos_atualizado
            }
          return render(request, "listargrupos.html",context)

