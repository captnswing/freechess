#-*- coding: utf-8 -*-
# settings/test.py
from .base import *

# http://stackoverflow.com/a/3098182/41404
# SOUTH_TESTS_MIGRATE = False
TEST_NAME = None
DATABASES = {
    'default':
        {
            'ENGINE': 'django.db.backends.sqlite3'
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
