
import horizon
from django.utils.translation import ugettext_lazy as _
from horizon_monitoring import dashboard


class ClientsPanel(horizon.Panel):
    name = _("Monitored Clients")
    slug = 'clients'

dashboard.MonitoringDashboard.register(ClientsPanel)
