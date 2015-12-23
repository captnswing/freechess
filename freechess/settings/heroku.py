# -*- coding: utf-8 -*-
# settings/heroku.py
from .base import *  # noqa

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {
    'default': dj_database_url.config()
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# debug
# heroku config:add DJANGO_DEBUG=true
# heroku config:remove DJANGO_DEBUG
DEBUG = bool(os.environ.get('DJANGO_DEBUG', ''))
