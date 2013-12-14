
from django.utils.translation import ugettext_lazy as _
from horizon import tables

class NoActionDataTable(tables.DataTable):
    """
    https://ask.openstack.org/en/question/1572/how-to-add-data-to-tables-in-horizon-dashboard/
    """

    def get_object_id(self, datum):
        return datum['name']

    def get_object_display(self, datum):
        return datum['name']
