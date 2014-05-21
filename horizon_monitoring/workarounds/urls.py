
from django.conf.urls import *
from .views import IndexView, UpdateView, CreateView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^workaround/(?P<id>[\w\.\-]+)/detail/$', UpdateView.as_view(), name='update'),
    url(r'^workaround/(?P<id>[\w\.\-]+)/create/$', CreateView.as_view(), name='create'),
)
