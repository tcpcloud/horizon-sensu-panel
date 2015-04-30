
from horizon import tables

from horizon_monitoring.stashes.tables import SensuStashesTable
from horizon_monitoring.api import sensu_api


class IndexView(tables.DataTableView):
    table_class = SensuStashesTable
    template_name = 'horizon_monitoring/stashes/index.html'

    def get_data(self):
        return sensu_api.stash_list
