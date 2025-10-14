from .settings_base import *

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
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    },
}

DATABASES = {
    'default': BANCOS['mysql'],
}

DEV = False
if DEV:
    DATABASES = {
        'default': BANCOS['postgres'],
    }
    MEDIA_ROOT = '/home/dev/code/media'
    STATIC_ROOT = '/home/dev/code/static'
    ALLOWED_HOSTS += ['localhost']