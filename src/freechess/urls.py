#-*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from freechess.stats import stats, images
from freechess.data import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# from http://www.arthurkoziel.com/2009/01/15/passing-mediaurl-djangos-500-error-view/
handler500 = 'freechess.stats.util.server_error'

# index
urlpatterns = patterns('',
   url(r'^$', stats.chessStats, name='stats-index'),
   url(r'^pythonversion', stats.pythonversion, name='stats-pythonversion'),
)

# images
urlpatterns += patterns('',
    url(r'monthlyresult.png$', images.monthlyResultImg, name='stats-monthlyresult'),
    url(r'opponentselo.png$', images.opponentsEloImg, name='stats-opponentselo'),
    url(r'elohist.png$', images.eloHistImg, name='stats-elohist'),
    url(r'elohist_highcharts.png$', images.eloHistImgHighCharts, name='stats-elohist-highcharts'),
)

# data admin
urlpatterns += patterns('',
    url(r'deletedata/$', views.deletedata, name='stats-deletedata'),
    url(r'uploaddata/$', views.upload_file, name='stats-uploadfile'),
)

urlpatterns += staticfiles_urlpatterns()