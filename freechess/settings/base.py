# -*- coding: utf-8 -*-
# Django settings for freechess project.
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
SECRET_KEY = '=s6(fo!)zvh0qo#3)mxo3_c!oaw(jo&plyr!mtpens)-h8j*51'
ALLOWED_HOSTS = []

ADMINS = ((u'Frank Hoffsümmer', 'frank.hoffsummer@gmail.com'),)
APPEND_SLASH = True
MANAGERS = ADMINS
TIME_ZONE = 'Europe/Stockholm'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
ADMIN_MEDIA_PREFIX = '/admin_media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': '5432'
    }
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Absolute path to the directory that holds user uploaded files
MEDIA_ROOT = os.path.join(BASE_DIR, "uploaded_pgnfiles")

# URL that handles the media served from MEDIA_ROOT
MEDIA_URL = '/pgnfiles/'

# installed apps
ROOT_URLCONF = 'freechess.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'freechess',
)

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
