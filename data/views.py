#-*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.http import condition
from django.http import HttpResponse
from pgnparser import parsePGNdata
from django.template.context import RequestContext
from freechess.stats.models import ChessGame, PGNfile
from django.forms import ModelForm
from django.core.urlresolvers import reverse

class UploadFileForm(ModelForm):
    class Meta:
        model = PGNfile

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            pgnfile = request.FILES['pgnfile']
            player = form.cleaned_data['player']
            allgames = parsePGNdata(pgnfile.read(), player)
#            form.save()
            ChessGame.objects.all().delete()
            for game in allgames:
                _result = ChessGame.objects.create(**game)
            return HttpResponseRedirect(reverse('stats-index'))
    else:
        form = UploadFileForm()
    return render_to_response('data.html', {'form': form}, context_instance=RequestContext(request))

@condition(etag_func=None)
def deletedata(request):
    ChessGame.objects.all().delete()
    return HttpResponse("deleted all data")
