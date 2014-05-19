
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import horizon

try:
    host = settings.KEDB_HOST
    include_kedb = True
except:
    include_kedb = False

if include_kedb:
    monitoring_panels = ('events', 'errors', 'stashes', 'checks', 'clients', 'info', 'workarounds', )
else:
    monitoring_panels = ('events', 'stashes', 'checks', 'clients', 'info', )

class MonitoringPanels(horizon.PanelGroup):
    slug = "monitoring"
    name = _("Monitoring")
    panels = monitoring_panels

class MonitoringDashboard(horizon.Dashboard):
    name = _("Monitoring")
    slug = "monitoring"
    panels = (MonitoringPanels,)
    default_panel = 'events'
#    permissions = ('openstack.roles.admin',)

horizon.register(MonitoringDashboard)
