from django.core.urlresolvers import reverse_lazy
from horizon import tables
from horizon import forms
from horizon import workflows
from horizon import exceptions
from horizon import messages

from horizon_monitoring.utils.gitlab_client import gitlab_api

from .tables import ProjectsTable

class IndexView(tables.DataTableView):
    table_class = ProjectsTable
    template_name = 'horizon_monitoring/gitlab/projects/index.html'

    def get_data(self):
        return gitlab_api.project_list(self.request)