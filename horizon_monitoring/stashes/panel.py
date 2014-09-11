
from django.utils.translation import ugettext_lazy as _

import horizon

from horizon_monitoring import dashboard


class StashesPanel(horizon.Panel):
    name = _("Event Stashes")
    slug = 'stashes'

dashboard.MonitoringDashboard.register(StashesPanel)
