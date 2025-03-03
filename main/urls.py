from django.contrib import admin
from django.urls import path, include
from main.apps.home.views import Home, UserChangePassword


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view()),
    path('home/', Home.as_view(), name='home'),
    path('user/', include('main.apps.home.urls')),
    path('changepassword/', include('django.contrib.auth.urls')),
    path('externaluser/', include('main.apps.externaluser.urls')),
    path('instance', include('main.apps.whatsapp.urls')),
    path('administracao/', include('main.apps.administracao.urls')),
    path('api/v1/', include('main.apps.webhook.urls'))
    
]
