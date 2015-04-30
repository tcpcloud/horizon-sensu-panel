
from django.utils.translation import ugettext_lazy as _
import horizon
from horizon_monitoring.dashboard import MonitoringDashboard, include_kedb
from django.conf import settings

from horizon_contrib.panel import ModelPanel


class WorkaroundsPanel(ModelPanel):
    name = _("Workarounds")
    slug = 'workarounds'

    #model_class = 'workaround'

if include_kedb:
    MonitoringDashboard.register(WorkaroundsPanel)
