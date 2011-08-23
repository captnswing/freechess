#-*- coding: utf-8 -*-
from django.conf import settings
from django import http
from django.template import Context, loader
import sys

# from http://www.arthurkoziel.com/2009/01/15/passing-mediaurl-djangos-500-error-view/
def server_error(request, template_name='500.html'):
    """
    500 error handler.

    Templates: `500.html`
    Context:
        STATIC_URL
            Path of static media (e.g. "/static/")
    """
    t = loader.get_template(template_name) # You need to create a 500.html template.
    return http.HttpResponseServerError(t.render(Context({
        'STATIC_URL': settings.STATIC_URL
    })))

def createhist(seq, binsize):
    h = {}
    for elem in seq:
        bin = divmod(elem, binsize)[0] * binsize
        h[bin] = h.get(bin, 0) + 1
    return h

def pythonversion(request):
    return http.HttpResponse(sys.version)
