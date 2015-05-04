
from django.utils.translation import ugettext_lazy as _
import horizon
from horizon_monitoring.dashboard import MonitoringDashboard, include_kedb
from django.conf import settings



class WorkaroundsPanel(horizon.Panel):
    name = _("Workarounds")
    slug = 'workarounds'


if include_kedb:
    MonitoringDashboard.register(WorkaroundsPanel)
