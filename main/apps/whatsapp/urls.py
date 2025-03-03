from django.urls import path
from .views import Instanceadd, Instancedelete,Instanceconect, Instancedesconect,Instancestatus,InstanceGroupList, InstanceGroupSync, InstanceRecreate,MsgList


urlpatterns = [
    path("add", Instanceadd.as_view(), name="instanceadd"),
    path("recreate/<int:id>", InstanceRecreate.as_view(), name="instancerecreate"),
    path("status/<int:id>", Instancestatus.as_view(), name="instancestatus"),
    path("conect/<int:id>", Instanceconect.as_view(), name="instanceconect"),
    path("desconect/<int:id>", Instancedesconect.as_view(), name="instancedesconect"),
    path("delete/<int:id>", Instancedelete.as_view(), name="instancedelete"),
    path("mensagem/list/<int:id>", MsgList.as_view(), name="instancemensagemlist"),


    path("group/list/<int:id>", InstanceGroupList.as_view(), name="instancegrouplist"),
    path("group/sync/<int:id>", InstanceGroupSync.as_view(), name="instancegroupsync")

]