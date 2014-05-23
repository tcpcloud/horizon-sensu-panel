
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import horizon

try:
    host = settings.KEDB_HOST
    include_kedb = True
except:
    include_kedb = False

class MonitoringPanels(horizon.PanelGroup):
    slug = "monitoring"
    name = _("Service Monitoring")
    panels =  ('events', 'stashes', 'checks', 'clients', 'info', )

class KEDBPanels(horizon.PanelGroup):
    slug = "kedb"
    name = _("Known Errors DB")
    panels = ('errors', 'workarounds',)

class MonitoringDashboard(horizon.Dashboard):
    name = _("Monitoring")
    slug = "monitoring"
    if include_kedb:
        panels = (MonitoringPanels, KEDBPanels)
    else:
        panels = (MonitoringPanels)

    default_panel = 'events'
#    permissions = ('openstack.roles.admin',)

horizon.register(MonitoringDashboard)
