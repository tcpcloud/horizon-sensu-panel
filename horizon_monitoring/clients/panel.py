
from django.utils.translation import ugettext_lazy as _
from horizon import Panel
from horizon_monitoring import dashboard


class ClientsPanel(Panel):
    name = _("Monitored Clients")
    slug = 'clients'

    model_class = 'client'

dashboard.MonitoringDashboard.register(ClientsPanel)
