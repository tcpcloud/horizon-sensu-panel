
from django.utils.translation import ugettext_lazy as _

import horizon

from horizon_monitoring import dashboard


class EventsPanel(horizon.Panel):
    name = _("Current Events")
    slug = 'events'

dashboard.MonitoringDashboard.register(EventsPanel)
