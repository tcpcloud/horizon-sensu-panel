
from django.utils.translation import ugettext_lazy as _
from horizon import tables

class SensuChecksTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_("Name"))
    command = tables.Column('command', verbose_name=_("Command"))
    subscribers = tables.Column('subscribers', verbose_name=_("Subscribers"))
    interval = tables.Column('interval', verbose_name=_("Interval"))

    def get_object_id(self, datum):
        return datum['name']

    def get_object_display(self, datum):
        return datum['name']

    class Meta:
        name = "checks"
        verbose_name = _("Checks")

