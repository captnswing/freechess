#!/Users/frank/.virtualenvs/djangy/bin/python
import os
import django.core.handlers.wsgi
import sys

path = '/Users/frank/Development/djangy'
if path not in sys.path:
    sys.path.append(path)

os.environ['PYTHON_EGG_CACHE'] = '/tmp'
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

application = django.core.handlers.wsgi.WSGIHandler()
