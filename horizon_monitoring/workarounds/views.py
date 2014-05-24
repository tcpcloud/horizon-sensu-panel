from django.core.urlresolvers import reverse_lazy
from horizon import tables
from horizon import forms
from horizon_monitoring.utils.kedb_client import kedb_api

from .tables import WorkaroundTable
from .forms import WorkaroundDetailForm, WorkaroundCreateForm, WorkaroundUpdateForm

class IndexView(tables.DataTableView):
    table_class = WorkaroundTable
    template_name = 'horizon_monitoring/workarounds/index.html'

    def get_data(self):
        return kedb_api.workaround_list

class CreateView(forms.ModalFormView):
    form_class = WorkaroundCreateForm
    template_name = 'horizon_monitoring/workarounds/create.html'
    success_url = reverse_lazy("horizon:monitoring:workarounds:index")
    
    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['known_error'] = self.kwargs['id']
        context['form_url_action'] = self.success_url
        return context

    def get_initial(self):
        return self.get_context_data()

class CreateFromErrorView(CreateView):
    template_name = 'horizon_monitoring/errors/workaround_create.html'
    success_url = reverse_lazy("horizon:monitoring:errors:index")

class UpdateView(forms.ModalFormView):
    form_class = WorkaroundUpdateForm
    template_name = 'horizon_monitoring/workarounds/update.html'
    success_url = reverse_lazy("horizon:monitoring:workarounds:index")
    
    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['workaround'] = kedb_api.workaround_update(self.kwargs['id'])
        context['workaround_id'] = self.kwargs['id']
        return context

    def get_initial(self):
        return self.get_context_data()["workaround"]