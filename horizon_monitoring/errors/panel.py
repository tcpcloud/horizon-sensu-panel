
import horizon
from django.utils.translation import ugettext_lazy as _
from horizon_monitoring import dashboard

class KedbErrorsPanel(horizon.Panel):
    name = _("Known Errors")
    slug = 'errors'

dashboard.MonitoringDashboard.register(KedbErrorsPanel)