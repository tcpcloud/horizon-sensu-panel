
from django.conf.urls import *
from .views import IndexView, DetailView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^error/(?P<id>[\w\.\-]+)/detail/$', DetailView.as_view(), name='detail'),
)
