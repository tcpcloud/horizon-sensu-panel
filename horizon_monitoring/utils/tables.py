
"""
https://ask.openstack.org/en/question/1572/how-to-add-data-to-tables-in-horizon-dashboard/
"""

from django.utils.translation import ugettext_lazy as _
from horizon import tables

class FilterAction(tables.FilterAction):

    def filter(self, table, objects, filter_string):
        q = filter_string.lower()

        def comp(service):
            if q in service.type.lower():
                return True
            return False

        return filter(comp, objects)