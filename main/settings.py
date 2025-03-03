from pathlib import Path

import os
# importar a biblioteca
from dotenv import load_dotenv
from decouple import config
from django.contrib.messages import constants

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# adicionar essa tag para que nosso projeto encontre o .env
load_dotenv(os.path.join(BASE_DIR, ".env"))

DEBUG = (os.getenv("DEBUG") == "True")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

APPEND_SLASH=False

# SECURITY WARNING: don't run with debug turned on in production!
# SECURITY WARNING: don't run with debug turned on in production!

#DEBUG = False

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000','https://*.marrera.net']


# Application definition

INSTALLED_APPS = [
    'rolepermissions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ninja_jwt',
    'ninja_extra',
    'rest_framework',
    # my apps 
    'main.apps.externaluser',
    'main.apps.whatsapp',
    'main.apps.administracao',
    'main.apps.home',
    'main.apps.webhook',
    #celery
    'django_celery_results',
    'django_celery_beat'
]


# CELERY BEAT SCHEDULER
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# REDIS CACHE

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://172.30.131.6:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'

]


AUTHENTICATION_BACKENDS = ['main.apps.externaluser.backends.EmailBackend']

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'

LANGUAGE_CODE = 'pt-BR'
USE_I18N = True

TIME_ZONE = 'America/Sao_Paulo'
USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
  'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': os.getenv('NAME_DB'),
	  'USER':os.getenv('USER_DB'),
	  'PASSWORD': os.getenv('PASSWORD_DB'),
	  'HOST':os.getenv('HOST_DB'),
	  'PORT':os.getenv('PORT_DB')

	}
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'requestlogs_to_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'info.log',
        },
    },
    'loggers': {
        'requestlogs': {
            'handlers': ['requestlogs_to_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}




# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# timeout tempo de inatividate no sistema
SESSION_EXPIRE_SECONDS = 1800 
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = 60  
SESSION_TIMEOUT_REDIRECT = 'https://app.marrera.net/accounts/login/'

# LOGIN
LOGOUT_REDIRECT_URL = 'login'
LOGIN_REDIRECT_URL = 'home'



# # Se tiver configuração de email
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = os.getenv('EMAIL_HOST')
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD') 
# EMAIL_PORT = os.getenv('EMAIL_PORT') 
# EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') 
# DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
# SERVER_EMAIL = DEFAULT_FROM_EMAIL


#SLEP_SEND_MSG
SLEEPMSG=config('SLEEPMSG')

# Se tiver configuração de email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD') 
EMAIL_PORT = os.getenv('EMAIL_PORT') 
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') 
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

#EVOLUTION
EVOLUTION_API_URL = config("EVOLUTION_API_URL")
EVOLUTIONMASTERKEY = config("EVOLUTIONMASTERKEY")