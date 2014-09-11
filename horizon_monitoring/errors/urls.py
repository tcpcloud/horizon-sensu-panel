
from django.conf.urls import *
from horizon_monitoring.errors.views import IndexView, CreateView, UpdateView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^error/(?P<id>[\w\.\-]+)/update/$', UpdateView.as_view(), name='update'),
    url(r'^error/create/$', CreateView.as_view(), name='create'),
    url(r'^error/(?P<check>[\w\.\-]+)/(?P<client>[\w\.\-]+)/create/$', CreateView.as_view(), name='create_check'),
)
