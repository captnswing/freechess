# -*- coding: utf-8 -*-
# settings/local.py
from .base import *  # noqa

DATABASES = {
    'default':
        {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'freechess.db'
        }
}

# debug
DEBUG = True
