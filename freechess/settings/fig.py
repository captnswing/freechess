# -*- coding: utf-8 -*-
import os
from .base import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_1_ENV_DB', 'postgres'),
        'USER': os.environ.get('DB_1_ENV_USER', 'postgres'),
        'HOST': os.environ.get('DB_1_PORT_5432_TCP_ADDR', 'localhost'),
        'PORT': os.environ.get('DB_1_PORT_5432_TCP_PORT', '5432'),
    }
}

# debug
DEBUG = True
TEMPLATE_DEBUG = DEBUG
