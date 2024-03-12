from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse

from .functions import ixc_sendtext

# Create your views here.
def ixc(requests):
    instanceName = (requests.GET['u'])
    recipientNumber = (requests.GET['to'])
    textMessage = (requests.GET['msg'])
    ixc_sendtext(instanceName, recipientNumber, textMessage)
    return HttpResponse('200') 