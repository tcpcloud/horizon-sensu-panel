
from django.utils.translation import ugettext_lazy as _
import horizon

class MonitoringDashboard(horizon.Dashboard):
    name = _("Monitoring")
    slug = "monitoring"

horizon.register(MonitoringDashboard)
