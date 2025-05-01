from .settings_base import *

BANCOS = {
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'abraao',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': 'localhost',
        'PORT': '3306',
    },
}

DATABASES = {
    'default': BANCOS['mysql'],
}

DEV = True
if DEV:
    DATABASES = {
        'default': BANCOS['postgres'],
    }
    MEDIA_ROOT = '/home/dev/code/media'
    STATIC_ROOT = '/home/dev/code/static'
    ALLOWED_HOSTS += ['localhost']