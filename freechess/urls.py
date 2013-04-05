#-*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


handler500 = 'freechess.stats.util.server_error'

# index
urlpatterns = patterns('freechess.stats',
    url(r'^$', 'stats.chessStats', name='stats-index'),
    url(r'^pythonversion', 'util.pythonversion', name='stats-pythonversion'),
)

# api
urlpatterns += patterns('',
    url(r'^api/', include('freechess.api.urls')),
)

if settings.DEBUG:
    # testing flot.js
    urlpatterns += patterns('',
        url('^flot/$', direct_to_template, { 'template': 'flot.html' }),
        url(r'^500/$', 'django.views.generic.simple.direct_to_template', {'template': '500.html'}),
        url(r'^404/$', 'django.views.generic.simple.direct_to_template', {'template': '404.html'})
    )

urlpatterns += staticfiles_urlpatterns()
