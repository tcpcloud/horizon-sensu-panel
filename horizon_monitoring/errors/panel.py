
import horizon
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from horizon_monitoring.dashboard import include_kedb, MonitoringDashboard


class KedbErrorsPanel(horizon.Panel):
    name = _("Known Errors")
    slug = 'errors'
    model_class = 'error'

if include_kedb:
    MonitoringDashboard.register(KedbErrorsPanel)
