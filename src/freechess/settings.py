#-*- coding: utf-8 -*-
# Django settings for freechess project.
ADMINS = (
    (u'Frank Hoffsümmer', 'frank.hoffsummer@gmail.com'),
)

APPEND_SLASH = True

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Stockholm'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=s6(fo!)zvh0qo#3)mxo3_c!oaw(jo&plyr!mtpens)-h8j*51'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'freechess.urls'

# current directory
import os
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

FIXTURE_DIRS = (os.path.join(PROJECT_PATH, "data", "fixtures"),)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

# Absolute path to the directory that holds user uploaded files
MEDIA_ROOT = os.path.join(PROJECT_PATH, "pgnfiles")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/pgnfiles/'


DATABASE_SUPPORTS_TRANSACTIONS = False

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'freechess.fileupload',
    'freechess.stats',
    'freechess.api',
)

# database configuration
import sys
DATABASES = {
    'default': {
        # https://docs.djangoproject.com/en/dev/ref/settings/#test-name
        'ENGINE': 'sqlite3' if 'test' in sys.argv else 'django.db.backends.postgresql_psycopg2',
        'NAME': 'captnswing',
        'USER': 'root',
        'PASSWORD': 'mp109',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# debug
DEBUG = True
TEMPLATE_DEBUG = True

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, "site_media"),
)

STATIC_URL = '/static/'
#  _            _                      __
# | |_ ___  ___| |_    ___ ___  _ __  / _|
# | __/ _ \/ __| __|  / __/ _ \| '_ \| |_
# | ||  __/\__ \ |_  | (_| (_) | | | |  _|
# \__\___||___/\__|  \___\___/|_| |_|_|
#
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--verbosity=0', ] #'--pdb']
INSTALLED_APPS += (
    'django_nose',
)
