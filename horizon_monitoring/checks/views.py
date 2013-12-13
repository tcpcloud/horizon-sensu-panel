
from horizon import tables
from .tables import SensuChecksTable
from horizon_monitoring.utils.sensu_client import sensu

class IndexView(tables.DataTableView):
    table_class = SensuChecksTable
    template_name = 'horizon_monitoring/checks/index.html'

    def get_data(self):
        return sensu.check_list()
