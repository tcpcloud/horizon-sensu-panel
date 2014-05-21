from django.core.urlresolvers import reverse_lazy
from horizon import tables
from horizon import forms
from horizon_monitoring.utils.kedb_client import kedb_api

from .tables import WorkaroundTable
from .forms import WorkaroundDetailForm, WorkaroundCreateForm

class IndexView(tables.DataTableView):
    table_class = WorkaroundTable
    template_name = 'horizon_monitoring/workarounds/index.html'

    def get_data(self):
        return kedb_api.workaround_list

class DetailView(forms.ModalFormView):
    form_class = WorkaroundDetailForm
    template_name = 'horizon_monitoring/workarounds/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['object'] = kedb_api.workaround_detail(workaround=self.kwargs['id'])
        return context

    def get_initial(self):
        return self.get_context_data()['object']

class CreateView(forms.ModalFormView):
    form_class = WorkaroundCreateForm
    template_name = 'horizon_monitoring/errors/create.html'
    success_url = reverse_lazy("horizon:monitoring:workarounds:index")
    
    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['known_error'] = self.kwargs['id']
        return context

    def get_initial(self):
        return self.get_context_data()