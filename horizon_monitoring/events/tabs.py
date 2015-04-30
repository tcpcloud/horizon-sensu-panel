
from django.utils.translation import ugettext_lazy as _
from horizon import tabs

from horizon_monitoring.workarounds.tables import WorkaroundTable


class OverviewTab(tabs.Tab):
    name = _("Overview")
    slug = "overview"
    template_name = ("horizon_monitoring/events/_detail_overview.html")

    def get_context_data(self, request):
        return {"instance": self.tab_group.kwargs['instance']}


class WorkaroundTab(tabs.TableTab):
    table_classes = (WorkaroundTable,)
    name = _("Workarounds")
    slug = "workarounds"
    template_name = "horizon_monitoring/events/_detail_workarounds.html"
    preload = True

    def get_workarounds_data(self):
        return self.tab_group.kwargs['instance'].get("workarounds", [])


class SensuEventDetailTabs(tabs.TabGroup):
    slug = "event_detail"
    tabs = (OverviewTab, WorkaroundTab,)
    sticky = True
