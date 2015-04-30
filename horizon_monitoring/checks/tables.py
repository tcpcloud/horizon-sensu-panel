
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _
from horizon import tables
from horizon_monitoring.templatetags.unit import join_list_with_newline
from horizon_monitoring.utils.actions import FilterAction


class RequestCheck(tables.LinkAction):
    name = "request_check"
    verbose_name = _("Request Check")
    url = "horizon:monitoring:checks:request"
    classes = ("ajax-modal", "btn-edit")

    def get_link_url(self, check):
        return urlresolvers.reverse(self.url, args=[check['name']])


class SensuChecksTable(tables.DataTable):

    name = tables.Column('name', verbose_name=_("Name"))
    subscribers = tables.Column('subscribers', verbose_name=_(
        "Subscribers"), filters=(join_list_with_newline,))
    handlers = tables.Column('handlers', verbose_name=_(
        "Handlers"), filters=(join_list_with_newline,))
    interval = tables.Column('interval', verbose_name=_("Interval"))
    command = tables.Column('command', verbose_name=_("Command"))
    customer = tables.Column('customer', verbose_name=_("Customer"))
    asset = tables.Column('asset', verbose_name=_("Asset"))

    def get_object_id(self, datum):
        return datum['name']

    def get_object_display(self, datum):
        return datum['name']

    class Meta:
        name = "checks"
        model_class = 'check'
        verbose_name = _("Service Checks Database")
        row_actions = (RequestCheck,)
        table_actions = (FilterAction,)
