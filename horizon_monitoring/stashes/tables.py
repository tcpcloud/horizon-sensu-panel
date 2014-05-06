
from django.core import urlresolvers
from django.template.defaultfilters import timesince
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from horizon import tables

from horizon_monitoring.utils.filters import timestamp_to_datetime, \
    nonbreakable_spaces, join_list_with_comma, unit_times

class ReasonColumn(tables.Column):

    def get_raw_data(self, datum):
        return datum['content']['reason']

class CreatedColumn(tables.Column):

    def get_raw_data(self, datum):
        return datum['content']['timestamp']

class SensuStashesTable(tables.DataTable):
    path = tables.Column('path', verbose_name=_("Path"), )
    reason = ReasonColumn('content', verbose_name=_("Reason"),)
    created = CreatedColumn('created', verbose_name=_("Created"), filters=(timestamp_to_datetime, timesince, nonbreakable_spaces) )
    expire = tables.Column('expire', verbose_name=_("Expires"), )

    def get_object_id(self, datum):
        return datum['path']

    class Meta:
        name = "stashes"
        verbose_name = _("Stashes")
