
from django.conf.urls import *
from .views import IndexView, FullScreenIndexView, DetailView, SilenceView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^fullscreen/$', FullScreenIndexView.as_view(), name='fullscreen_index'),
    url(r'^events/(?P<check>[\w\-\_\.]+)/(?P<client>[\w\.\-]+)/detail/$', DetailView.as_view(), name='detail'),
    url(r'^events/(?P<check>[\w\-\_\.]+)/(?P<client>[\w\.\-]+)/(?P<dc>[\w\.\-]+)/detail/$', DetailView.as_view(), name='detail'),
    url(r'^events/(?P<check>[\w\-\_\.]+)/silence-check/$', SilenceView.as_view(), name='silence_check'),
    url(r'^events/(?P<check>[\w\-\_\.]+)/(?P<dc>[\w\-\_\.]+)/silence-check/$', SilenceView.as_view(), name='silence_check'),
    url(r'^events/(?P<client>[\w\-\_\.]+)/silence-client/$', SilenceView.as_view(), name='silence_client'),
    url(r'^events/(?P<client>[\w\-\_\.]+)/(?P<dc>[\w\-\_\.]+)/silence-client/$', SilenceView.as_view(), name='silence_client'),
    url(r'^events/(?P<client>[\w\-\_\.]+)/(?P<check>[\w\.\-]+)/silence-client-check/$', SilenceView.as_view(), name='silence_client_check'),
    url(r'^events/(?P<client>[\w\-\_\.]+)/(?P<check>[\w\.\-]+)/(?P<dc>[\w\-\_\.]+)/silence-client-check/$', SilenceView.as_view(), name='silence_client_check'),
)
