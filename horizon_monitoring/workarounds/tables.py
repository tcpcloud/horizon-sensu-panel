from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _
from horizon import tables
from horizon_monitoring.api import kedb_api
from horizon_monitoring.utils import FilterAction


class WorkaroundDetail(tables.LinkAction):

    """workaround detail
    """
    name = "workaround_detail"
    verbose_name = _("Workaound detail")
    classes = ("ajax-modal", "btn-edit")

    def get_link_url(self, workaround):
        url = "horizon:monitoring:workarounds:detail"

        return urlresolvers.reverse(url, args=(workaround.get("id"),))

    def allowed(self, request, instance):
        return True


class WorkaroundUpdate(tables.LinkAction):

    """workaround detail
    """
    name = "workaround_update"
    verbose_name = _("Workaround update")
    classes = ("ajax-modal", "btn-edit")

    def get_link_url(self, workaround):
        url = "horizon:monitoring:workarounds:update"

        return urlresolvers.reverse(url, args=(workaround.get("id"),))

    def allowed(self, request, instance):
        return True


class WorkaroundDelete(tables.DeleteAction):

    data_type_singular = _("Workaround")
    data_type_plural = _("Workarounds")

    def delete(self, request, obj_id):
        kedb_api.workaround_delete(obj_id)

    def allowed(self, request, instance):
        return True


class ErrorColumn(tables.base.Column):

    def get_raw_data(self, datum):
        error_detail = datum.get("error_detail", None)
        if error_detail:
            return error_detail.get("name")
        return ""


class WorkaroundTable(tables.DataTable):

    def get_error_link(self):
        url = "horizon:monitoring:errors:update"
        error_id = self.get("error_detail").get("id")
        return urlresolvers.reverse(url, args=(error_id,))

    id = tables.Column('id', verbose_name=_("ID"))
    known_error = ErrorColumn(
        'known_error_name', verbose_name=_("Known error"))
    description = tables.Column('description', verbose_name=_("Description"))
    action = tables.Column('action', verbose_name=_("Action"))
    engine = tables.Column('engine', verbose_name=_("Engine"))

    def get_object_id(self, datum):
        return datum['id']

    def get_object_display(self, datum):
        return datum['id']

    class Meta:
        name = "workarounds"
        verbose_name = _("Workarounds list")
        row_actions = (WorkaroundUpdate, WorkaroundDelete)
        table_actions = (WorkaroundDelete, FilterAction)
