#-*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from freechess import stats, data, api
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# from http://www.arthurkoziel.com/2009/01/15/passing-mediaurl-djangos-500-error-view/
handler500 = 'freechess.stats.util.server_error'

# index
urlpatterns = patterns('',
   url(r'^$', stats.stats.chessStats, name='stats-index'),
   url(r'^pythonversion', stats.util.pythonversion, name='stats-pythonversion'),
)

# images
urlpatterns += patterns('',
    url(r'monthlyresult.png$', stats.images.monthlyResultImg, name='stats-monthlyresult'),
    url(r'opponentselo.png$', stats.images.opponentsEloImg, name='stats-opponentselo'),
    url(r'elohist.png$', stats.images.eloHistImg, name='stats-elohist'),
    url(r'elohist_highcharts.png$', stats.images.eloHistImgHighCharts, name='stats-elohist-highcharts'),
)

# data admin
urlpatterns += patterns('',
    url(r'deletedata/$', data.views.deletedata, name='stats-deletedata'),
    url(r'uploaddata/$', data.views.upload_file, name='stats-uploadfile'),
)

# api
urlpatterns += patterns('',
   url(r'^api/', include('freechess.api.urls')),
)

# static files
urlpatterns += staticfiles_urlpatterns()