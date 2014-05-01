import datetime
import logging

from django.utils.translation import ugettext as _

import horizon
from horizon import tables

from openstack_dashboard import api

from .tables import SensuInfoTable

from horizon_monitoring.utils.sensu_client import sensu_api


logger = logging.getLogger(__name__)

class InfoView(tables.DataTableView):
    table_class = SensuInfoTable
    template_name = 'horizon_monitoring/info/index.html'

    def get_context_data(self, **kwargs):
        context = super(tables.DataTableView, self).get_context_data(**kwargs)

        if hasattr(self, "table"):
            context[self.context_object_name] = self.table
        
        return context

    def get_data(self):
        return sensu_api.service_status
