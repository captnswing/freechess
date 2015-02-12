# -*- coding: utf-8 -*-
from django.conf import settings
from django import http
from django.template import Context, loader


def server_error(request):
    """
    custom 500 error handler, that includes STATIC_URL in context
    """
    t = loader.get_template('500.html')
    return http.HttpResponseServerError(t.render(Context({
        'STATIC_URL': settings.STATIC_URL
    })))


def createhist(seq, binsize):
    h = {}
    for elem in seq:
        hbin = divmod(elem, binsize)[0] * binsize
        h[hbin] = h.get(hbin, 0) + 1
    return h
