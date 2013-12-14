
from horizon import tables
from .tables import SensuEventsTable
from horizon_monitoring.utils.sensu_client import sensu_api

class IndexView(tables.DataTableView):
    table_class = SensuEventsTable
    template_name = 'horizon_monitoring/events/index.html'

    def get_data(self):
        return sensu_api.event_list
