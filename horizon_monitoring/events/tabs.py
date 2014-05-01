
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api

class OverviewTab(tabs.Tab):
    name = _("Overview")
    slug = "overview"
    template_name = ("horizon_monitoring/events/_detail_overview.html")

    def get_context_data(self, request):
        return {"instance": self.tab_group.kwargs['instance']}

class WorkaroundTab(tabs.Tab):
    name = _("Console")
    slug = "console"
    template_name = "horizon_monitoring/events/_detail_console.html"
    preload = False

    def get_context_data(self, request):
        instance = self.tab_group.kwargs['instance']
        # Currently prefer VNC over SPICE, since noVNC has had much more
        # testing than spice-html5
        console_type = getattr(settings, 'CONSOLE_TYPE', 'AUTO')

        return {'console_url': console_type, 'instance_id': instance.id}

class SensuEventDetailTabs(tabs.TabGroup):
    slug = "event_detail"
    tabs = (OverviewTab, WorkaroundTab,)
    sticky = True
