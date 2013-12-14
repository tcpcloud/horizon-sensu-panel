
from django.utils.translation import ugettext_lazy as _
import horizon

class MonitoringDashboard(horizon.Dashboard):
    name = _("Monitoring")
    slug = "monitoring"
    panels = ('checks',)
    default_panel = 'checks'
#    permissions = ('openstack.roles.admin',)

horizon.register(MonitoringDashboard)
