
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

from horizon_monitoring.events.tables import SensuEventsTable
from horizon_monitoring.events.tabs import SensuEventDetailTabs
from horizon_monitoring.utils.sensu_client import sensu_api

class IndexView(tables.DataTableView):
    table_class = SensuEventsTable
    template_name = 'horizon_monitoring/events/index.html'

    def get_data(self):
        return sensu_api.event_list

def event_detail(request, check, client):
    template_name = 'horizon_monitoring/events/detail.html'

    response = {}

    return render_to_response(template_name, response, RequestContext(request))
"""
class RebuildView(forms.ModalFormView):
    form_class = project_forms.RebuildInstanceForm
    template_name = 'project/instances/rebuild.html'
    success_url = reverse_lazy('horizon:project:instances:index')

    def get_context_data(self, **kwargs):
        context = super(RebuildView, self).get_context_data(**kwargs)
        context['instance_id'] = self.kwargs['instance_id']
        context['can_set_server_password'] = api.nova.can_set_server_password()
        return context

    def get_initial(self):
        return {'instance_id': self.kwargs['instance_id']}


class UpdateView(workflows.WorkflowView):
    workflow_class = project_workflows.UpdateInstance
    success_url = reverse_lazy("horizon:project:instances:index")

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context["instance_id"] = self.kwargs['instance_id']
        return context

    @memoized.memoized_method
    def get_object(self, *args, **kwargs):
        instance_id = self.kwargs['instance_id']
        try:
            return api.nova.server_get(self.request, instance_id)
        except Exception:
            redirect = reverse("horizon:project:instances:index")
            msg = _('Unable to retrieve instance details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        initial = super(UpdateView, self).get_initial()
        initial.update({'instance_id': self.kwargs['instance_id'],
                'name': getattr(self.get_object(), 'name', '')})
        return initial
"""

class DetailView(tabs.TabView):
    tab_group_class = SensuEventDetailTabs
    template_name = 'horizon_monitoring/events/detail.html'
    redirect_url = 'horizon:monitoring:events:index'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context["instance"] = self.get_data()
        return context

    def get_data(self):
        instance_id = self.kwargs['check']
        try:
            event = sensu_api.event_list
        except Exception:
            redirect = reverse(self.redirect_url)
            exceptions.handle(self.request,
                              _('Unable to retrieve details for '
                                'instance "%s".') % instance_id,
                                redirect=redirect)
            # Not all exception types handled above will result in a redirect.
            # Need to raise here just in case.
            raise exceptions.Http302(redirect)
        return event

    def get_tabs(self, request, *args, **kwargs):
        instance = self.get_data()
        return self.tab_group_class(request, instance=instance, **kwargs)