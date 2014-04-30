
from horizon import tables
from .tables import KedbErrorsTable
from horizon_monitoring.utils.kedb_client import kedb_api

class IndexView(tables.DataTableView):
    table_class = KedbErrorsTable
    template_name = 'horizon_monitoring/errors/index.html'

    def get_data(self):
        return kedb_api.error_list
