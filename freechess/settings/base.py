#-*- coding: utf-8 -*-
# Django settings for freechess project.
from os.path import join, abspath, dirname
root = lambda *x: join(abspath(dirname(__file__)), '..', *x)

DEBUG = False
TEMPLATE_DEBUG = DEBUG
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
TEMPLATE_DIRS = (root("templates"),)
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
    'django.core.context_processors.static',
)

# Absolute path to the directory that holds user uploaded files
MEDIA_ROOT = root("uploaded_pgnfiles")

# URL that handles the media served from MEDIA_ROOT
MEDIA_URL = '/pgnfiles/'

# installed apps
ROOT_URLCONF = 'freechess.urls'
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'freechess.main',
)

# staticfiles
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    root('static-media'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
