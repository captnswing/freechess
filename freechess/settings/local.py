#-*- coding: utf-8 -*-
# settings/local.py
from .base import *

DATABASES = {
    'default':
        {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'freechess.db'
        }
}

# debug
DEBUG = True
TEMPLATE_DEBUG = DEBUG
