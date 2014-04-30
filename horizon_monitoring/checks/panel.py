
import horizon
from django.utils.translation import ugettext_lazy as _
from horizon_monitoring import dashboard

class ChecksPanel(horizon.Panel):
    name = _("Check Definitions")
    slug = 'checks'

dashboard.MonitoringDashboard.register(ChecksPanel)