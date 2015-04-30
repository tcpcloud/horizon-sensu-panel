from django.core.urlresolvers import reverse_lazy
from horizon import forms, tables
from horizon_monitoring.api import kedb_api, sensu_api
from horizon_monitoring.workarounds.tables import WorkaroundTable

from .forms import (ErrorCheckCreateForm, ErrorCreateForm,
                    UpdateErrorForm)
from .tables import KedbErrorsTable


class IndexView(tables.DataTableView):
    table_class = KedbErrorsTable
    template_name = "horizon_monitoring/errors/index.html"

    def get_data(self):
        return kedb_api.error_list


class UpdateView(forms.ModalFormView):
    template_name = "horizon_monitoring/errors/update.html"
    form_class = UpdateErrorForm
    success_url = reverse_lazy("horizon:monitoring:errors:index")

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['error'] = kedb_api.error_update(self.kwargs['id'])
        context['workarounds'] = WorkaroundTable(request=self.request,
                                                 data=context['error'].get("workarounds", []))
        return context

    def get_initial(self, **kwargs):
        error = self.get_context_data()["error"]
        error["id"] = self.kwargs['id']
        return error


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
            context["output_pattern"] = sensu_api.event_detail(
                check, client)['check']['output']
        return context

    def get_initial(self):
        return self.get_context_data()
