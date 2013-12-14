
from django.utils.translation import ugettext_lazy as _
from horizon import tables
from horizon_monitoring.utils.tables import NoActionDataTable

class SensuChecksTable(NoActionDataTable):
    name = tables.Column('name', verbose_name=_("name"))
    command = tables.Column('command', verbose_name=_("Command"))
    subscribers = tables.Column('subscribers', verbose_name=_("Subscribers"))
    interval = tables.Column('interval', verbose_name=_("Interval"))

    class Meta:
        name = "checks"
        verbose_name = _("Checks")
