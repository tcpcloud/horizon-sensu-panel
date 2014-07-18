from django.core.urlresolvers import reverse_lazy
from horizon import tables
from horizon import forms
from horizon import workflows
from horizon import exceptions
from horizon import messages

from horizon_monitoring.utils.kedb_client import kedb_api
from horizon_monitoring.utils.sensu_client import sensu_api

from .tables import KedbErrorsTable
from horizon_monitoring.workarounds.tables import WorkaroundTable
from .forms import ErrorDetailForm, ErrorCreateForm, ErrorCheckCreateForm
from .workflows import UpdateError

class IndexView(tables.DataTableView):
    table_class = KedbErrorsTable
    template_name = 'horizon_monitoring/errors/index.html'

    def get_data(self):
        return kedb_api.error_list

class UpdateView(workflows.WorkflowView):
    
    workflow_class = UpdateError
    #template_name = 'horizon_monitoring/errors/update.html'

    """
    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['error'] = kedb_api.error_detail(self.kwargs['id'])
        context['workarounds'] = context['error'].get("workarounds", [])
        return context
    """

    def get_initial(self, **kwargs):
        context = super(UpdateView, self).get_initial(**kwargs)
        #context['id'] = self.kwargs['id']
        context['error'] = kedb_api.error_update(self.kwargs['id'])
        #context['workarounds'] = context['error'].get("workarounds", [])
        #context['workarounds_table'] = WorkaroundTable(request=self.request, data=context['workarounds'])
        return context["error"]

class CreateView(forms.ModalFormView):

    form_class = ErrorCheckCreateForm
    template_name = 'horizon_monitoring/errors/create.html'
    success_url = reverse_lazy("horizon:monitoring:events:index")

    def get_form_class(self):
        if not self.get_context_data().get("check", None):
            self.success_url = reverse_lazy("horizon:monitoring:errors:index")
            return ErrorCreateForm
        return self.form_class

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        check = self.kwargs.get("check", None)
        client = self.kwargs.get("client", None)
        if check and client:
            context["check"] = check
            context["client"] = client
            context["output_pattern"] = sensu_api.event_detail(check, client)["output"]
        return context

    def get_initial(self):
        return self.get_context_data()
