from django.shortcuts import render, redirect
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from whatsapp.models import whatsapp
from .functions import get_all_grupos
from django.contrib import auth,messages
from django.core.paginator import Paginator


# Create your views here.

@login_required
def listar_grupos(request):
    zap = whatsapp.objects.filter(usuario=request.user, status="open")
    context = {
            'page_title': 'Listar grupos',
            'zap': zap
            } 
    if request.method == "POST":
        instancia_nome = (request.POST['pesquisa'])
        instancia = whatsapp.objects.get(nome=instancia_nome)
        response = (get_all_grupos(instancia.key))
        if response.status_code == 200:
            grupo_list = []
            for grupo in response.json():
                grupo_list.append({"id": grupo['id'].replace("@g.us", ""),"subject": grupo['subject']})
            context = {
               "grupos": grupo_list,
               "zap": zap
            }
            return render(request, "grupos/listargrupos.html",context)
        else:
            messages.error(request, "Não foi possível listar seus grupos. Verifique se sua instância está conectada ou entre em contato com o suporte")
            return render(request, "grupos/listargrupos.html",context)
    return render(request, "grupos/listargrupos.html", context)
      





