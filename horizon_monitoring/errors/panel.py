
import horizon
from django.utils.translation import ugettext_lazy as _
from horizon_monitoring import dashboard

class ErrorsPanel(horizon.Panel):
    name = _("Known Error Database")
    slug = 'errors'

dashboard.MonitoringDashboard.register(ErrorsPanel)