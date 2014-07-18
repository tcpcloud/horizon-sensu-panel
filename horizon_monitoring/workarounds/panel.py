
from django.utils.translation import ugettext_lazy as _
import horizon
from horizon_monitoring.dashboard import MonitoringDashboard
from django.conf import settings

try:
    host = settings.KEDB_HOST
    include_kedb = True
except:
    include_kedb = False

class WorkaroundsPanel(horizon.Panel):
    name = _("Workarounds")
    slug = 'workarounds'

if include_kedb:
    MonitoringDashboard.register(WorkaroundsPanel)
