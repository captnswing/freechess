#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'freechess.settings.heroku'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
