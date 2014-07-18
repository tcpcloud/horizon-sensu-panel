# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from horizon import tables

class SensuInfoTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_('Name'))
    value = tables.Column('value', verbose_name=_('Value'))

    def get_object_id(self, datum):
        return datum['name']

    class Meta:
        name = "info"
        verbose_name = _("Monitoring Service Status")
