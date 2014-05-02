
import horizon
from django.utils.translation import ugettext_lazy as _
from horizon_monitoring import dashboard

try:
    host = settings.KEDB_HOST
    include_kedb = True
except:
    include_kedb = False

class KedbErrorsPanel(horizon.Panel):
    name = _("Known Errors")
    slug = 'errors'

if include_kedb:
    dashboard.MonitoringDashboard.register(KedbErrorsPanel)
