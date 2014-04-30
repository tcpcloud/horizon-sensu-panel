
from django.utils.translation import ugettext_lazy as _
from horizon import tables

class KedbErrorsTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_("Name"))
    check = tables.Column('check', verbose_name=_("Check"))
    severity = tables.Column('severity', verbose_name=_("Severity"))
    level = tables.Column('level', verbose_name=_("Resolves"))

    def get_object_id(self, datum):
        return datum['name']

    def get_object_display(self, datum):
        return datum['name']

    class Meta:
        name = "clients"
        verbose_name = _("Clients")

