
from horizon import tables
from horizon import forms
from .tables import KedbErrorsTable
from horizon_monitoring.utils.kedb_client import kedb_api

from horizon_monitoring.errors.forms import ErrorDetailForm

class IndexView(tables.DataTableView):
    table_class = KedbErrorsTable
    template_name = 'horizon_monitoring/errors/index.html'

    def get_data(self):
        return kedb_api.error_list

class DetailView(forms.ModalFormView):
    """view pro zobrazeni modalni okna pro vyber sablony 
    ktere redirectne na samotny render sablony
    """
    form_class = ErrorDetailForm
    template_name = 'horizon_monitoring/errors/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['error'] = kedb_api.error_detail(error=self.kwargs['id'])
        return context

    def get_initial(self):
        error = self.get_context_data()['error']
        return error