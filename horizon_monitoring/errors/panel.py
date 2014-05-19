
from django.utils.translation import ugettext_lazy as _
import horizon
from horizon_monitoring.dashboard import MonitoringDashboard
from django.conf import settings

try:
    host = settings.KEDB_HOST
    include_kedb = True
except:
    include_kedb = False

class KedbErrorsPanel(horizon.Panel):
    name = _("Known Errors")
    slug = 'errors'

if include_kedb:
    MonitoringDashboard.register(KedbErrorsPanel)
