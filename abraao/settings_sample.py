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

DEV = False
if DEV:
    DATABASES = {
        'default': BANCOS['mysql'],
    }
    MEDIA_ROOT = '/home/dev/code/media'
    STATIC_ROOT = '/home/dev/code/static'
    ALLOWED_HOSTS += ['localhost']