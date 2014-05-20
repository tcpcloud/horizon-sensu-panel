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

class WorkaroundTable(tables.DataTable):

    id = tables.Column('id', verbose_name=_("ID"))
    description = tables.Column('description', verbose_name=_("Description"))
    known_error = tables.Column('known_error', verbose_name=_("Known_error"))
    
    def get_object_id(self, datum):
        return datum['id']

    def get_object_display(self, datum):
        return datum['id']

    class Meta:
        name = "workarounds"
        verbose_name = _("Workarounds list")
        row_actions = (WorkaroundDetail, )
