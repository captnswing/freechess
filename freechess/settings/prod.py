#!/usr/bin/env python
#-*- coding: utf-8 -*-

# settings/prod.py
from .base import *

# # database configuration
# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = dict()
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# DATABASE_SUPPORTS_TRANSACTIONS = False
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'captnswing',
#         'USER': 'root',
#         'PASSWORD': 'mp109',
#         'HOST': '',
#         'PORT': '',
#     }
# }

# debug
DEBUG = False
TEMPLATE_DEBUG = DEBUG
