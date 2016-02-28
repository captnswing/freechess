# -*- coding: utf-8 -*-
from django.conf.urls import *  # noqa
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import admin

handler500 = 'freechess.main.util.server_error'

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       )

urlpatterns += patterns('freechess',
                        url(r'^$', 'stats.chessStats', name='main-index'),
                        url(r'^api/elohist', 'api.elohist', name='api-elohist'),
                        url(r'^api/monthlyresult', 'api.monthlyresult', name='api-monthlyresult'),
                        url(r'^api/opponentselo', 'api.opponentselo', name='api-opponentselo')
                        )

if settings.DEBUG:
    urlpatterns += patterns('',
                            # testing flot.js
                            url('^flot/$', TemplateView.as_view(template_name='flot.html')),
                            # testing custom error pages
                            url(r'^500/$', TemplateView.as_view(template_name='500.html')),
                            url(r'^404/$', TemplateView.as_view(template_name='404.html'))
                            )
