#!/usr/bin/env python
#-*- coding: utf-8 -*-

# settings/test.py
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

# debug
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# test
FIXTURE_DIRS = (root("fixtures"),)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--verbosity=0', ] #'--pdb']
INSTALLED_APPS += ('django_nose',)
