
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import horizon

include_kedb = False

if hasattr(settings, "KEDB_HOST"):
    include_kedb = True


class MonitoringPanels(horizon.PanelGroup):
    slug = "monitoring"
    name = _("Service Monitoring")
    panels = ('events', 'stashes', 'checks', 'clients', 'aggregates', 'info', )


class KEDBPanels(horizon.PanelGroup):
    slug = "kedb"
    name = _("Known Errors DB")
    panels = ('errors', 'workarounds',)


class MonitoringDashboard(horizon.Dashboard):
    name = _("Monitoring")
    slug = "monitoring"
    icon = "fa fa-area-chart"

    if include_kedb:
        panels = (MonitoringPanels, KEDBPanels, )
    else:
        panels = (MonitoringPanels,)

    permissions = ('openstack.roles.admin',)
    default_panel = 'events'
#    permissions = ('openstack.roles.admin',)

horizon.register(MonitoringDashboard)
