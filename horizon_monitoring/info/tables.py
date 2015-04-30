# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from horizon import tables
from horizon_monitoring.utils import sensu_settings


class SensuInfoTable(tables.DataTable):
    redis = tables.Column('redis', verbose_name=_(
        'Redis'), filters=(lambda t: t['connected'],))
    transport = tables.Column('transport', verbose_name=_(
        'RabbitMQ'), filters=(lambda t: t['connected'],))
    version = tables.Column(
        'sensu', verbose_name=_('Version'), filters=(lambda s: s['version'],))

    if sensu_settings.SENSU_MULTI:
        dc = tables.Column('datacenter', verbose_name=_('Datacenter'))

    def get_object_id(self, datum):
        return datum.get('datacenter', datum['sensu']['version'])

    class Meta:
        name = "info"
        verbose_name = _("Monitoring Service Status")
