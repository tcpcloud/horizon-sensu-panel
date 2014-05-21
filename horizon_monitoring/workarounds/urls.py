
from django.conf.urls import *
from .views import IndexView, DetailView, CreateView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^workaround/(?P<id>[\w\.\-]+)/detail/$', DetailView.as_view(), name='detail'),
    url(r'^workaround/(?P<id>[\w\.\-]+)/create/$', CreateView.as_view(), name='create'),
)
