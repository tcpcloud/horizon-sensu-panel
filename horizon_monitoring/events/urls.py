
from django.conf.urls import *
from .views import IndexView, DetailView, ResolveView, SilenceClientView, SilenceCheckView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^events/(?P<check>[\w\_]+)/(?P<client>[\w\.\-]+)/detail/$', DetailView.as_view(), name='detail'),
    url(r'^events/(?P<check>[\w\_]+)/(?P<client>[\w\.\-]+)/resolve/$', ResolveView.as_view(), name='resolve'),
    url(r'^events/(?P<check>[\w\_]+)/(?P<client>[\w\.\-]+)/silence-check/$', SilenceCheckView.as_view(), name='silence_check'),
    url(r'^events/(?P<check>[\w\_]+)/(?P<client>[\w\.\-]+)/silence-client/$', SilenceClientView.as_view(), name='silence_client'),
)
