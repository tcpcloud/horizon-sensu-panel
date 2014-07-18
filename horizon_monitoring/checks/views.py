
from django import http
from django import shortcuts
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import tables
from horizon import forms

from horizon_monitoring.checks.tables import SensuChecksTable
from horizon_monitoring.checks.forms import RequestCheckForm
from horizon_monitoring.utils.sensu_client import sensu_api

class IndexView(tables.DataTableView):
    table_class = SensuChecksTable
    template_name = 'horizon_monitoring/checks/index.html'

    def get_data(self):
        return sensu_api.check_list

class RequestView(forms.ModalFormView):
    form_class = RequestCheckForm
    template_name = 'horizon_monitoring/checks/request.html'
    success_url = reverse_lazy('horizon:monitoring:checks:index')

    def get_context_data(self, **kwargs):
        context = super(RequestView, self).get_context_data(**kwargs)
        context['check'] = self.kwargs['check']
        return context

    def get_initial(self):
        return {
            'check': self.kwargs['check'],
        }
