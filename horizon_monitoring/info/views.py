import logging

import six
from horizon import tables
from horizon_monitoring.utils import sensu_settings
from horizon_monitoring.api import sensu_api

from .tables import SensuInfoTable

logger = logging.getLogger(__name__)


class InfoView(tables.DataTableView):
    table_class = SensuInfoTable
    template_name = 'horizon_monitoring/info/index.html'

    def get_data(self):
        data = []
        if sensu_settings.SENSU_MULTI:
            for dc, config in six.iteritems(sensu_settings.SENSU_API):
                sensu_api.set_sensu_api(config)
                datum = sensu_api.service_status
                datum['datacenter'] = dc
                data += [datum]
        else:
            data = [sensu_api.service_status]
        return data
