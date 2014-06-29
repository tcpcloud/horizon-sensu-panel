# -*- coding: UTF-8 -*-
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _
from horizon import tables
from horizon_contrib.tables.actions import FilterAction

class KeysTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_("ID"))
    title = tables.Column('title', verbose_name=_("Title"))
    key = tables.Column('key', verbose_name=_("Key"))
    #created_at = tables.Column('created_at', verbose_name=_("Created at"))

    def get_object_id(self, datum):
        return datum['id']

    def get_object_display(self, datum):
        return datum['title']

    class Meta:
        name = "keys"
        verbose_name = _("Deploy Keys")
        table_actions= (FilterAction, )
