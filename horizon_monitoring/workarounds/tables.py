from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _
from horizon import tables

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

class ErrorColumn(tables.Column):

    def get_raw_data(self, datum):
        return datum["error_detail"]["name"]

class WorkaroundTable(tables.DataTable):

    def get_error_link(self):
        url = "horizon:monitoring:errors:update"
        error_id = self.get("error_detail").get("id")
        return urlresolvers.reverse(url, args=(error_id,))

    id = tables.Column('id', verbose_name=_("ID"))
    description = tables.Column('description', verbose_name=_("Description"))
    known_error = ErrorColumn('known_error', verbose_name=_("Known_error"), link=get_error_link)
    action = tables.Column('action', verbose_name=_("Action"))
    engine = tables.Column('engine', verbose_name=_("Engine"))
    
    def get_object_id(self, datum):
        return datum['id']

    def get_object_display(self, datum):
        return datum['id']

    class Meta:
        name = "workarounds"
        verbose_name = _("Workarounds list")
        row_actions = (WorkaroundDetail, )
