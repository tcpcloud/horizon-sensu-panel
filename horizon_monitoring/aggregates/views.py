
from horizon import tables
from horizon_monitoring.utils import sensu_api

from .tables import AggregatesTable


class IndexView(tables.DataTableView):
    table_class = AggregatesTable
    template_name = 'horizon_monitoring/aggregates/index.html'

    def get_data(self):
        return sensu_api.aggregates
