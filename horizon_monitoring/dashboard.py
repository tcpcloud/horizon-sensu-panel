
from django.utils.translation import ugettext_lazy as _
import horizon

class MonitoringPanels(horizon.PanelGroup):
    slug = "monitoring"
    name = _("Monitoring Panel")
    panels = ('checks', )

class MonitoringDashboard(horizon.Dashboard):
    name = _("Monitoring")
    slug = "monitoring"
    panels = (MonitoringPanels,)
    default_panel = 'checks'
    permissions = ('openstack.roles.admin',)

horizon.register(MonitoringDashboard)
