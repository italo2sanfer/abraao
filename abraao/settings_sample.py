from .settings_base import *
import os

BANCOS = {
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'db',
        'PORT': '5432',
    },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': os.environ.get('MYSQL_DATABASE'),
        'USER': os.environ.get('MYSQL_USER'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
        'HOST': os.environ.get('MYSQL_HOST', 'db_mysql'),
        'PORT': '3306',
    },
}

DATABASES = {
    'default': BANCOS['mysql'],
}

PASSAPP_API_TOKEN = "token-producao-aqui"
MEDIA_ROOT = '/home/Italo2sanfer/abraao/media'
STATIC_ROOT = '/home/Italo2sanfer/abraao/static'

DEV = False
if DEV:
    PASSAPP_API_TOKEN = "token-desenvolvimento-aqui"
    # Em DEV, permitir todos (mais simples). Em produção especifique origens seguras em CORS_ALLOWED_ORIGINS
    CORS_ALLOW_ALL_ORIGINS = True
    DATABASES = {
        'default': BANCOS['mysql'],
    }
    MEDIA_ROOT = '/home/dev/code/media'
    STATIC_ROOT = '/home/dev/code/static'
    ALLOWED_HOSTS += ['localhost']

TOKEN_EXPIRY = 1200  # 20 minutos em segundos