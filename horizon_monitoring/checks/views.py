
import six
from django.core.urlresolvers import reverse_lazy
from horizon import forms, messages, tables
from horizon_monitoring.checks.forms import RequestCheckForm
from horizon_monitoring.checks.tables import SensuChecksTable
from horizon_monitoring.utils import sensu_settings
from horizon_monitoring.api import sensu_api


class IndexView(tables.DataTableView):
    table_class = SensuChecksTable
    template_name = 'horizon_monitoring/checks/index.html'

    def get_data(self):
        """ return tagged events from all sensu APIs
        iterate and create clients for every sensu
        load events and tag it with sensu name
        """
        data = []

        if sensu_settings.SENSU_MULTI:
            for dc, config in six.iteritems(sensu_settings.SENSU_API):
                try:
                    sensu_api.set_sensu_api(config)
                    _checks = sensu_api.check_list
                    checks = []
                    for c in _checks:
                        c['datacenter'] = dc
                        checks.append(c)
                    data += checks
                except Exception as e:
                    messages.error(self.request, '{} - {}'.format(dc, e))
        else:
            data = sensu_api.check_list
        return data


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
