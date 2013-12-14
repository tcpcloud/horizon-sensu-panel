
from django.utils.translation import ugettext_lazy as _
from horizon import tables

class SensuEventsTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_("Name"))
    command = tables.Column('command', verbose_name=_("Command"))
    subscribers = tables.Column('subscribers', verbose_name=_("Subscribers"))
    interval = tables.Column('interval', verbose_name=_("Interval"))

    def get_object_id(self, datum):
        return '%s-%s' % (datum['client'], datum['check'])

    def get_object_id(self, datum):
        return '%s-%s' % (datum['client'], datum['check'])

    class Meta:
        name = "checks"
        verbose_name = _("Checks")

