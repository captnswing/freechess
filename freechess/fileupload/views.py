from django.views.generic import CreateView, DeleteView
from django.http import HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.conf import settings
import os
from freechess.pgnparser import parsePGNfile
from freechess.stats.models import ChessGame, PGNfile

def handle_uploaded_file(filename):
    allgames = parsePGNfile(open(filename))
    ChessGame.objects.all().delete()
    for game in allgames:
        _result = ChessGame.objects.create(**game)


class PGNfileCreateView(CreateView):
    model = PGNfile

    def form_valid(self, form):
        self.object = form.save()
        # 'pgnfile' is the name of the input field in the form in the pgnfile_form.html template
        f = self.request.FILES.get('pgnfile')
        data = [{'name': f.name,
                 'url': os.path.join(settings.MEDIA_URL, f.name),
                 'delete_url': reverse('upload-delete', args=[self.object.id]),
                 'delete_type': "DELETE"}]
        handle_uploaded_file(os.path.join(settings.MEDIA_ROOT, f.name))
        response = JSONResponse(data, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PGNfileDeleteView(DeleteView):
    model = PGNfile

    def delete(self, request, *args, **kwargs):
        """
        This does not actually delete the file, only the database record. But
        that is easy to implement.
        """
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class JSONResponse(HttpResponse):
    """JSON response class."""

    def __init__(self, obj='', json_opts=dict(), mimetype="application/json", *args, **kwargs):
        content = simplejson.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)


def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"
