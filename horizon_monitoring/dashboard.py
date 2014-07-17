
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import horizon

include_kedb = False
include_gitlab = False

kedb = getattr(settings, "KEDB_HOST", None)
gitlab = getattr(settings, "GITLAB_PORT", None)

if kedb:
    include_kedb = True

if gitlab:
    include_gitlab = True

class MonitoringPanels(horizon.PanelGroup):
    slug = "monitoring"
    name = _("Service Monitoring")
    panels =  ('events', 'stashes', 'checks', 'clients', 'info', )

class KEDBPanels(horizon.PanelGroup):
    slug = "kedb"
    name = _("Known Errors DB")
    panels = ('errors', 'workarounds',)

class GitlabPanels(horizon.PanelGroup):
    slug = "gitlab"
    name = _("Gitlab")
    panels = ('projects', 'keys')

class MonitoringDashboard(horizon.Dashboard):
    name = _("Monitoring")
    slug = "monitoring"
    if include_kedb and include_gitlab:
        panels = (MonitoringPanels, KEDBPanels, GitlabPanels, )
    elif include_kedb:
        panels = (MonitoringPanels, KEDBPanels, )
    elif include_gitlab:
        panels = (MonitoringPanels, GitlabPanels)
    else:
        panels = (MonitoringPanels)

    default_panel = 'events'
#    permissions = ('openstack.roles.admin',)

horizon.register(MonitoringDashboard)
