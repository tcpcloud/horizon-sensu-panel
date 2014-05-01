
from django.conf.urls import *
from .views import IndexView, DetailView, ResolveView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^events/(?P<check>[\w\_]+)/(?P<client>[\w\.\-]+)/detail/$', DetailView.as_view(), name='detail'),
    url(r'^events/(?P<check>[\w\_]+)/(?P<client>[\w\.\-]+)/resolve/$', ResolveView.as_view(), name='resolve'),
)
