
from django.utils.translation import ugettext_lazy as _
import horizon

class MonitoringPanels(horizon.PanelGroup):
    slug = "monitoring"
    name = _("Monitoring Panel")
    panels = ('events', 'errors', 'checks', 'clients', )

class MonitoringDashboard(horizon.Dashboard):
    name = _("Monitoring")
    slug = "monitoring"
    panels = (MonitoringPanels,)
    default_panel = 'events'
    permissions = ('openstack.roles.admin',)

horizon.register(MonitoringDashboard)
