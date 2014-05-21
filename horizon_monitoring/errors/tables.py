# -*- coding: UTF-8 -*-
from django.core import urlresolvers
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext_lazy as _
from horizon import tables
from horizon.tables import formset
from horizon_monitoring.workarounds.forms import WorkaroundDetailForm
from horizon_monitoring.utils.kedb_client import kedb_api

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

class ErrorDelete(tables.DeleteAction):
    """error delete
    """
    data_type_singular = _("Error")
    data_type_plural = _("Errors")

    def delete(self, request, obj_id):
        kedb_api.error_delete(request, obj_id)

    def allowed(self, request, instance):
        return True

class ErrorCreate(tables.LinkAction):
    """error create
    """
    name = "error_create"
    verbose_name = _("Create Error")
    classes = ("ajax-modal", "btn-edit")

    def get_link_url(self):
        url = "horizon:monitoring:errors:create"
        return urlresolvers.reverse(url, args=[])

    def allowed(self, request, instance):
        return True

class WorkaroundCreate(tables.LinkAction):
    """workaround create
    """
    name = "workaround_create"
    verbose_name = _("Create Workaround")
    classes = ("ajax-modal", "btn-edit")

    def get_link_url(self, error):
        url = "horizon:monitoring:workarounds:create"
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
    ownership = tables.Column('ownership', verbose_name=_("Ownership"))

    def get_object_id(self, datum):
        return datum['id']

    def get_object_display(self, datum):
        return datum['name']

    class Meta:
        name = "errors"
        verbose_name = _("Known Errors Database")
        row_actions = (ErrorUpdate, WorkaroundCreate, ErrorDelete )
        table_actions= (ErrorCreate, )

WorkaroundsFormSet = formset_factory(WorkaroundDetailForm)
from random import randint

class KedbErrorsFormsetTable(formset.FormsetDataTable):
    formset_class = WorkaroundsFormSet

    def get_object_display(self, datum):
        return datum

    def get_object_id(self, datum):
        return datum

    class Meta:
        name = "workarounds"
        verbose_name = _("WorkaroundsFormSet")