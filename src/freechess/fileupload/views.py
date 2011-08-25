#-*- coding: utf-8 -*-
from django.utils import simplejson
from django.http import HttpResponse
from freechess.fileupload.models import PGNfile
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DeleteView
from django.conf import settings
import os


def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    return "text/plain"


class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='', json_opts=dict(), mimetype="application/json", *args, **kwargs):
        content = simplejson.dumps(obj, **json_opts)
        super(JSONResponse,self).__init__(content, mimetype, *args, **kwargs)


class PGNfileCreateView(CreateView):

    model = PGNfile

    def form_valid(self, form):
        self.object = form.save()
        f = self.request.FILES.get('file')
        data = [{'name': f.name,
                'url': os.path.join(settings.MEDIA_URL, f.name),
                'thumbnail_url': os.path.join(settings.MEDIA_URL, f.name),
                'delete_url': reverse('upload-delete', args=[self.object.id]),
                'delete_type': "DELETE"}]
        response = JSONResponse(data, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PGNfileDeleteView(DeleteView):

    model = PGNfile

    def delete(self, request, *args, **kwargs):
        """This does not actually delete the file, only the database record. But
        that is easy to implement."""
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

