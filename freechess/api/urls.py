#-*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('freechess.api.handlers',
    url(r'^elohist', 'elohist', name='api-elohist'),
    url(r'^monthlyresult', 'monthlyresult', name='api-monthlyresult'),
    url(r'^opponentselo', 'opponentselo', name='api-opponentselo'),
)
