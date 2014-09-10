
from django.conf.urls.defaults import *
from .views import InfoView

urlpatterns = patterns('horizon_monitoring',
    url(r'^$', InfoView.as_view(), name='index')
)