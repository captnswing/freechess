from django.conf.urls.defaults import *
from freechess.fileupload.views import PGNfileCreateView, PGNfileDeleteView

urlpatterns = patterns('',
    (r'^new/$', PGNfileCreateView.as_view(), {}, 'upload-new'),
    (r'^delete/(?P<pk>\d+)$', PGNfileDeleteView.as_view(), {}, 'upload-delete'),
)
