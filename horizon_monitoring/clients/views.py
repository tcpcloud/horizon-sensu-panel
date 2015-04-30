
from horizon import tables
from .tables import SensuClientsTable
from horizon_monitoring.api import sensu_api


class IndexView(tables.DataTableView):
    table_class = SensuClientsTable
    template_name = 'horizon_monitoring/clients/index.html'

    def get_data(self):
        return sensu_api.client_list
