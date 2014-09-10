
from django.conf.urls import *
from horizon_monitoring.workarounds.views import IndexView, UpdateView, CreateView, CreateFromErrorView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^workaround/(?P<id>[\w\.\-]+)/detail/$', UpdateView.as_view(), name='update'),
    url(r'^workaround/(?P<id>[\w\.\-]+)/create/$', CreateView.as_view(), name='create'),
    url(r'^error/workaround/(?P<id>[\w\.\-]+)/create/$', CreateFromErrorView.as_view(), name='create_from_error'),
)
