#-*- coding: utf-8 -*-
# Django settings for freechess project.
import os
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

ADMINS = ((u'Frank Hoffsümmer', 'frank.hoffsummer@gmail.com'),)
APPEND_SLASH = True
MANAGERS = ADMINS
TIME_ZONE = 'Europe/Stockholm'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
ADMIN_MEDIA_PREFIX = '/admin_media/'
SECRET_KEY = '=s6(fo!)zvh0qo#3)mxo3_c!oaw(jo&plyr!mtpens)-h8j*51'
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

# templates
TEMPLATE_DIRS = (os.path.join(PROJECT_PATH, "templates"),)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

# Absolute path to the directory that holds user uploaded files
MEDIA_ROOT = os.path.join(PROJECT_PATH, "pgnfiles")

# URL that handles the media served from MEDIA_ROOT
MEDIA_URL = '/pgnfiles/'

# installed apps
ROOT_URLCONF = 'freechess.urls'
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'freechess.fileupload',
    'freechess.stats',
    'freechess.api',
)

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
DEBUG = True
TEMPLATE_DEBUG = True

# staticfiles
STATIC_URL = '/static/'
INSTALLED_APPS += ('django.contrib.staticfiles',)
STATICFILES_DIRS = (os.path.join(PROJECT_PATH, "site_media"),)
TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.static',)

# test
FIXTURE_DIRS = (os.path.join(PROJECT_PATH, "data", "fixtures"),)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--verbosity=0', ] #'--pdb']
INSTALLED_APPS += ('django_nose',)
