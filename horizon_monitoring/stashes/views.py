
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
from horizon_monitoring.stashes.forms import DeleteStashForm
from horizon_monitoring.utils.sensu_client import sensu_api

class IndexView(tables.DataTableView):
    table_class = SensuStashesTable
    template_name = 'horizon_monitoring/stashes/index.html'

    def get_data(self):
        return sensu_api.stash_list

class DeleteView(forms.ModalFormView):
    form_class = DeleteStashForm
    template_name = 'horizon_monitoring/stashes/delete.html'
    success_url = reverse_lazy('horizon:monitoring:stashes:index')

    def get_context_data(self, **kwargs):
        context = super(DeleteView, self).get_context_data(**kwargs)
        context['path'] = self.kwargs['path']
        return context

    def get_initial(self):
        return {
            'path': self.kwargs['path'],
        }
