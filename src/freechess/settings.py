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

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/sitemedia'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=s6(fo!)zvh0qo#3)mxo3_c!oaw(jo&plyr!mtpens)-h8j*51'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.load_template_source',
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

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "templates"),
    os.path.join(PROJECT_PATH, "stats/templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
)

DATABASE_SUPPORTS_TRANSACTIONS = False

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'freechess.stats',
)

# database configuration
DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'captnswing'
DATABASE_USER = 'root'
DATABASE_PASSWORD = 'mp109'
DATABASE_HOST = ''
DATABASE_PORT = ''


# a directory "site_media" that contains the static media files should exist there
DEV_DOCROOT = os.path.join(PROJECT_PATH, "site_media")

# debug
DEBUG = True
TEMPLATE_DEBUG = True

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

#                 _
#  ___  ___ _ __ | |_ _ __ _   _
# / __|/ _ \ '_ \| __| '__| | | |
# \__ \  __/ | | | |_| |  | |_| |
# |___/\___|_| |_|\__|_|   \__, |
#                          |___/
#
#INSTALLED_APPS += (
#    'indexer',
#    'paging',
#    'sentry',
#    'sentry.client',
#)

#     _                                     ____ _____
#    / \   _ __ ___   __ _ _______  _ __   / ___|___ /
#   / _ \ | '_ ` _ \ / _` |_  / _ \| '_ \  \___ \ |_ \
#  / ___ \| | | | | | (_| |/ / (_) | | | |  ___) |__) |
# /_/   \_\_| |_| |_|\__,_/___\___/|_| |_| |____/____/
#
#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#AWS_ACCESS_KEY_ID = '12YAAWKJ7TJ7RZ0C1FG2'
#AWS_SECRET_ACCESS_KEY = '77x5r4wOED+Z8CjnFGMgSL77O2cInxs9Scd4HbOe'
#AWS_STORAGE_BUCKET_NAME = 'frank-data'
#from S3 import CallingFormat
#AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN
#
#INSTALLED_APPS += (
#    'storages',
#)


#   ____     _
#  / ___|___| | ___ _ __ _   _
# | |   / _ \ |/ _ \ '__| | | |
# | |__|  __/ |  __/ |  | |_| |
#  \____\___|_|\___|_|   \__, |
#                        |___/

#import djcelery
#INSTALLED_APPS += (
#   'djcelery',
#   'ghettoq',
#)
#djcelery.setup_loader()
#CELERY_IMPORTS = (
#   "stats.backgroundtasks",
#)
