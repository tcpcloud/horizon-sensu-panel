
from django.utils.translation import ugettext_lazy as _
from horizon_monitoring import dashboard

from horizon_contrib.panel import ModelPanel


class ChecksPanel(ModelPanel):
    name = _("Service Checks")
    slug = 'checks'

    model_class = 'check'

dashboard.MonitoringDashboard.register(ChecksPanel)
