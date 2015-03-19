
from django.utils.translation import ugettext_lazy as _
from horizon_contrib.panel import ModelPanel
from horizon_monitoring import dashboard


class ClientsPanel(ModelPanel):
    name = _("Monitored Clients")
    slug = 'clients'

    model_class = 'client'

dashboard.MonitoringDashboard.register(ClientsPanel)
