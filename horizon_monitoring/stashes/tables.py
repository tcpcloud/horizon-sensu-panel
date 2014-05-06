
from django.core import urlresolvers
from django.template.defaultfilters import timesince
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from horizon import tables

from horizon_monitoring.utils.filters import timestamp_to_datetime, \
    nonbreakable_spaces, join_list_with_comma, unit_times

class SensuStashesTable(tables.DataTable):
    path = tables.Column('path', verbose_name=_("Path"), )
    content = tables.Column('content', verbose_name=_("Content"),)
    expire = tables.Column('expire', verbose_name=_("Expire"), )

    def get_object_id(self, datum):
        return datum['path']

    class Meta:
        name = "stashes"
        verbose_name = _("Stashes")
