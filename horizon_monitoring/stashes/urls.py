

"""

# Key 	Description 	Owner 	Expires in 	Set 	Action

Enter key

Note: No spaces, etc e.g. "silence/client_name/check_name"


Description



Expire at (Optional):

"""

from django.conf.urls import *
from .views import IndexView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),

)
