# -*- coding: utf-8 -*-
from .base import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'dockerhost',
        'PORT': '32768',
    }
}

# debug
DEBUG = True
