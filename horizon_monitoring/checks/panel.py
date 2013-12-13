
import horizon
from django.utils.translation import ugettext_lazy as _
from horizon_monitoring import dashboard

class Checks(horizon.Panel):
    name = _("Checks")
    slug = 'checks'

dashboard.MonitoringDashboard.register(Checks)