#!/usr/bin/env python
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
