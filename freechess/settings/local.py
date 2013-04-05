#-*- coding: utf-8 -*-

# settings/local.py
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'freechess',
        'USER': 'root',
        'PASSWORD': 'mp109',
        'HOST': '',
        'PORT': '',
    }
}

# debug
DEBUG = True
TEMPLATE_DEBUG = DEBUG
