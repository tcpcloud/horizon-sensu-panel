
from django import http
from django import shortcuts
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import tables
from horizon import exceptions
from horizon import forms
from horizon import tabs
from horizon import workflows

from horizon_monitoring.stashes.tables import SensuStashesTable
from horizon_monitoring.utils.sensu_client import sensu_api


class IndexView(tables.DataTableView):
    table_class = SensuStashesTable
    template_name = 'horizon_monitoring/stashes/index.html'

    def get_data(self):
        return sensu_api.stash_list
