#!/usr/bin/env python
#-*- coding: utf-8 -*-

# settings/prod.py
from .base import *

# database configuration
DATABASE_SUPPORTS_TRANSACTIONS = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'captnswing',
        'USER': 'root',
        'PASSWORD': 'mp109',
        'HOST': '',
        'PORT': '',
    }
}


# debug
DEBUG = False
TEMPLATE_DEBUG = DEBUG
