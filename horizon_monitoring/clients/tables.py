
from django.utils.translation import ugettext_lazy as _
from horizon import tables

class SensuClientsTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_("Name"))
    address = tables.Column('address', verbose_name=_("Address"))
    subscriptions = tables.Column('subscriptions', verbose_name=_("Subscriptions"))
    timestamp = tables.Column('timestamp', verbose_name=_("Last reply"))

    def get_object_id(self, datum):
        return datum['name']

    def get_object_display(self, datum):
        return datum['name']

    class Meta:
        name = "clients"
        verbose_name = _("Clients")

