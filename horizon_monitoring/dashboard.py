
import horizon

class MonitoringDashboard(horizon.Dashboard):
    name = _("Monitoring")
    slug = "monitoring"


horizon.register(MonitoringDashboard)
