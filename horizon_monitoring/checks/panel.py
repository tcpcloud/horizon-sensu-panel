
from django.utils.translation import ugettext_lazy as _
from horizon_monitoring import dashboard

from horizon import Panel


class ChecksPanel(Panel):
    name = _("Service Checks")
    slug = 'checks'

dashboard.MonitoringDashboard.register(ChecksPanel)
