#-*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# from http://www.arthurkoziel.com/2009/01/15/passing-mediaurl-djangos-500-error-view/
handler500 = 'freechess.stats.util.server_error'

# index
urlpatterns = patterns('freechess.stats',
   url(r'^$', 'stats.chessStats', name='stats-index'),
   url(r'^pythonversion', 'util.pythonversion', name='stats-pythonversion'),
)

# data admin
urlpatterns += patterns('freechess.fileupload',
    url(r'^upload/', include('freechess.fileupload.urls')),
)

# api
urlpatterns += patterns('',
   url(r'^api/', include('freechess.api.urls')),
)

# static files
urlpatterns += staticfiles_urlpatterns()
