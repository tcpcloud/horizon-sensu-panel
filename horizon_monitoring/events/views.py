
import six
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions, forms, messages, tables, tabs
from horizon_monitoring.dashboard import include_kedb
from horizon_monitoring.events.forms import SilenceForm
from horizon_monitoring.events.tables import (FullScreenSensuEventsTable,
                                              SensuEventsTable)
from horizon_monitoring.events.tabs import SensuEventDetailTabs
from horizon_monitoring.utils import sensu_settings
from horizon_monitoring.api import kedb_api, sensu_api


class IndexView(tables.DataTableView):
    table_class = SensuEventsTable
    template_name = 'horizon_monitoring/events/index.html'

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
                    _events = sensu_api.event_list(self.request)
                    events = []
                    for event in _events:
                        event['datacenter'] = dc
                        events.append(event)
                    data += events
                except Exception as e:
                    messages.error(self.request, '{} - {}'.format(dc, e))
        else:
            data = sensu_api.event_list(self.request)
        return data


class FullScreenIndexView(IndexView):
    table_class = FullScreenSensuEventsTable
    template_name = 'horizon_monitoring/events/fullscreen.html'

    def filter_silenced(self, events):
        return [e for e in events if not e.get("silenced", False)]

    def get_data(self):
        events = super(FullScreenIndexView, self).get_data()
        return self.filter_silenced(events)


class SilenceView(forms.ModalFormView):
    form_class = SilenceForm
    template_name = 'horizon_monitoring/events/silence_check.html'
    success_url = reverse_lazy('horizon:monitoring:events:index')

    def get_context_data(self, **kwargs):
        context = super(SilenceView, self).get_context_data(**kwargs)
        context['check'] = self.kwargs.get("check", None)
        context['client'] = self.kwargs.get("client", None)
        context['dc'] = self.kwargs.get("dc", None)
        return context

    def get_initial(self):
        return self.get_context_data()


class DetailView(tabs.TabView):
    tab_group_class = SensuEventDetailTabs
    template_name = 'horizon_monitoring/events/detail.html'
    redirect_url = 'horizon:monitoring:events:index'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['check'] = self.kwargs['check']
        context['client'] = self.kwargs['client']
        dc = self.kwargs.get('dc', None)
        if dc and sensu_settings.SENSU_MULTI:
            context['datacenter'] = sensu_settings.SENSU_API.get(dc)

        return context

    def get_data(self):
        check = self.kwargs['check']
        client = self.kwargs['client']
        dc = self.kwargs.get('dc', None)
        if dc and sensu_settings.SENSU_MULTI:
            sensu_api.set_sensu_api(sensu_settings.SENSU_API.get(dc))

        try:
            event = sensu_api.event_detail(check, client)
            try:
                if include_kedb:
                    event = kedb_api.event_list([event])[0]
            except Exception as e:
                pass
        except Exception:
            redirect = reverse(self.redirect_url)
            exceptions.handle(self.request,
                              _('Unable to retrieve details for '
                                'instance "%s".') % check,
                              redirect=redirect)
            # Not all exception types handled above will result in a redirect.
            # Need to raise here just in case.
            raise exceptions.Http302(redirect)
        return event

    def get_tabs(self, request, *args, **kwargs):
        instance = self.get_data()
        return self.tab_group_class(request, instance=instance, **kwargs)
