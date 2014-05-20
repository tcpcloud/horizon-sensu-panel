# -*- coding: UTF-8 -*-
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _
from horizon import tables

class ErrorUpdate(tables.LinkAction):
    """error detail
    """
    name = "error_update"
    verbose_name = _("Error update")
    classes = ("ajax-modal", "btn-edit")

    def get_link_url(self, error):
        url = "horizon:monitoring:errors:update"
        return urlresolvers.reverse(url, args=(error.get("id"),))

    def allowed(self, request, instance):
        return True

class KedbErrorsTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    name = tables.Column('name', verbose_name=_("Name"))
    description = tables.Column('description', verbose_name=_("Description"))
    check = tables.Column('check', verbose_name=_("Check"))
    severity = tables.Column('severity', verbose_name=_("Severity"))
    level = tables.Column('level', verbose_name=_("Level"))

    def get_object_id(self, datum):
        return datum['name']

    def get_object_display(self, datum):
        return datum['name']

    class Meta:
        name = "errors"
        verbose_name = _("Known Errors Database")
        row_actions = (ErrorUpdate, )
