from django.shortcuts import render
from externaluser.models import perfil
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import auth,messages
from externaluser.forms import PerfilForm
from django.contrib.auth.models import User

# Create your views here.
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
       profile = perfil.objects.all()
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