
from django.utils.translation import ugettext_lazy as _
import horizon
from horizon_monitoring.dashboard import MonitoringDashboard, include_kedb
from django.conf import settings


class KedbErrorsPanel(horizon.Panel):
    name = _("Known Errors")
    slug = 'errors'

if include_kedb:
    MonitoringDashboard.register(KedbErrorsPanel)
