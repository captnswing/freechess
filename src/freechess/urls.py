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

# images
urlpatterns += patterns('freechess.stats',
    url(r'monthlyresult.png$', 'images.monthlyResultImg', name='stats-monthlyresult'),
    url(r'opponentselo.png$', 'images.opponentsEloImg', name='stats-opponentselo'),
    url(r'elohist.png$', 'images.eloHistImg', name='stats-elohist'),
    url(r'elohist_highcharts', 'images.eloHistImgHighCharts', name='stats-elohist-highcharts'),
)

# data admin
urlpatterns += patterns('freechess.fileupload',
    url(r'^upload/', include('fileupload.urls')),
)

# api
urlpatterns += patterns('',
   url(r'^api/', include('freechess.api.urls')),
)

# static files
urlpatterns += staticfiles_urlpatterns()