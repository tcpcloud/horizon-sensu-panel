
from django.utils.translation import ugettext_lazy as _
from horizon import tables

class SensuEventsTable(tables.DataTable):
    client = tables.Column('client', verbose_name=_("Client"))
    check = tables.Column('check', verbose_name=_("Check"))
    occurrences = tables.Column('occurrences', verbose_name=_("Occurrences"))
    output = tables.Column('output', verbose_name=_("Output"))
    status = tables.Column('status', verbose_name=_("Status"))
    flapping = tables.Column('flapping', verbose_name=_("Flapping"))

    def get_object_id(self, datum):
        return '%s-%s' % (datum['client'], datum['check'])

    def get_object_id(self, datum):
        return '%s-%s' % (datum['client'], datum['check'])

    class Meta:
        name = "checks"
        verbose_name = _("Checks")

