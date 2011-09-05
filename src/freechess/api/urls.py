#-*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from piston.resource import Resource
from freechess.api.handlers import ChessGameHandler

chessgame_resource = Resource(ChessGameHandler)

urlpatterns = patterns('',
    url(r'^elohist', chessgame_resource, { 'emitter_format': 'json' }),
)
