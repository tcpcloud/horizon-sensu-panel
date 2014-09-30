from django.conf.urls import patterns, url, include

from .views import InfoView

urlpatterns = patterns('horizon_monitoring',
    url(r'^$', InfoView.as_view(), name='index')
)