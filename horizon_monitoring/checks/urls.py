
from django.conf.urls import *
from .views import IndexView, RequestView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<check>[\w\-\_\.]+)/request/$', RequestView.as_view(), name='request'),
)
