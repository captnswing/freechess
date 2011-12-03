from django.conf.urls.defaults import *
from freechess.fileupload.views import PGNfileCreateView, PGNfileDeleteView

urlpatterns = patterns('',
    url(r'^new/$', PGNfileCreateView.as_view(), {}, name='upload-new'),
    url(r'^delete/(?P<pk>\d+)$', PGNfileDeleteView.as_view(), {}, name='upload-delete'),
)

