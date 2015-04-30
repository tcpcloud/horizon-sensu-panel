
from django.template.defaultfilters import timesince
from django.utils.translation import ugettext_lazy as _

from horizon import tables

from horizon_monitoring.templatetags.unit import timestamp_to_datetime, \
    nonbreakable_spaces, join_list_with_comma, unit_times

from horizon_monitoring.api import sensu_api
from horizon_monitoring.utils import FilterAction


class StashDelete(tables.DeleteAction):
    action_present = ("Delete",)
    action_past = ("Deleted",)
    data_type_singular = _("Stash")
    data_type_plural = _("stashes")
    name = "stash_delete"
    success_url = "horizon:monitoring:stashes:index"

    def delete(self, request, path):
        sensu_api.stash_delete(path)


class ReasonColumn(tables.Column):

    def get_raw_data(self, datum):
        return datum['content'].get('reason', "")


class CreatedColumn(tables.Column):

    def get_raw_data(self, datum):
        return datum['content']['timestamp']


class SensuStashesTable(tables.DataTable):
    path = tables.Column('path', verbose_name=_("Path"), )
    reason = ReasonColumn('content', verbose_name=_("Reason"),)
    created = CreatedColumn('created', verbose_name=_("Created"), filters=(
        timestamp_to_datetime, timesince, nonbreakable_spaces))
    expire = tables.Column('expire', verbose_name=_("Expires"), )

    def get_object_display(self, datum):
        return datum['path']

    def get_object_id(self, datum):
        return datum['path']

    class Meta:
        name = "stashes"
        verbose_name = _("Stashes")
        row_actions = (StashDelete, )
        table_actions = (StashDelete, FilterAction)
