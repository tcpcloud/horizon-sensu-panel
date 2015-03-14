
from django.utils.translation import ugettext_lazy as _

import horizon

from horizon_monitoring import dashboard


class AggregatesPanel(horizon.Panel):
    name = _("Aggregates")
    slug = 'aggregates'

dashboard.MonitoringDashboard.register(AggregatesPanel)
