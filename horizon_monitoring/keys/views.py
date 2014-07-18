from django.core.urlresolvers import reverse_lazy
from horizon import tables
from horizon import forms
from horizon import workflows
from horizon import exceptions
from horizon import messages

from horizon_monitoring.utils.gitlab_client import gitlab_api

from .tables import KeysTable

class IndexView(tables.DataTableView):
    table_class = KeysTable
    template_name = 'horizon_monitoring/gitlab/keys/index.html'

    def get_data(self):
        return gitlab_api.deploy_key_list(project_id=1)