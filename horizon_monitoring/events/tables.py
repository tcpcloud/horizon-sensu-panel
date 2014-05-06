
from django.core import urlresolvers
from django.template.defaultfilters import timesince
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from horizon import tables

from horizon_monitoring.utils.filters import timestamp_to_datetime, \
    nonbreakable_spaces, join_list_with_comma, unit_times

class FullScreenView(tables.LinkAction):
    name = "fullscreen_view"
    verbose_name = _("Fullscreen")
    url = "horizon:monitoring:events:fullscreen_index"
    classes = ("btn")

    def get_link_url(self):
        return urlresolvers.reverse(self.url, args=[])

class ResolveEvent(tables.LinkAction):
    name = "resolve_event"
    verbose_name = _("Resolve")
    url = "horizon:monitoring:events:resolve"
    classes = ("ajax-modal", "btn-edit")

    def get_link_url(self, event):
        return urlresolvers.reverse(self.url, args=[event['check'], event['client']])

class EventDetail(tables.LinkAction):
    name = "event_detail"
    verbose_name = _("Detail")
    url = "horizon:monitoring:events:detail"
    classes = ("btn-edit")

    def get_link_url(self, event):
        return self._get_link_url(event, 'overview')

    def _get_link_url(self, event, step_slug):
        base_url = urlresolvers.reverse(self.url, args=[event['check'], event['client']])
        param = urlencode({"step": step_slug})
        return "?".join([base_url, param])

    def allowed(self, request, instance):
        return True

class SilenceCheck(tables.LinkAction):
    name = "silence_check"  
    verbose_name = _("Silence Check")
    url = "horizon:monitoring:events:silence_check"
    classes = ("ajax-modal", "btn")

    def get_link_url(self, event):
        return urlresolvers.reverse(self.url, args=[event['check'], event['client']])

class SilenceClient(tables.LinkAction):
    name = "silence_client"  
    verbose_name = _("Silence Client")
    url = "horizon:monitoring:events:silence_client"
    classes = ("ajax-modal", "btn")

    def get_link_url(self, event):
        return urlresolvers.reverse(self.url, args=[event['check'], event['client']])

class SensuEventsTable(tables.DataTable):
    client = tables.Column('client', verbose_name=_("Client"))
    check = tables.Column('check', verbose_name=_("Check"))
    output = tables.Column('output', verbose_name=_("Output"), truncate=100)
    status = tables.Column('status', verbose_name=_("Status"), classes=('status_column',), hidden=True)
    flapping = tables.Column('flapping', verbose_name=_("Flapping"))
    occurrences = tables.Column('occurrences', verbose_name=_("Occured"), filters=(unit_times, ))
    issued = tables.Column('issued', verbose_name=_("Last occurence"), filters=(timestamp_to_datetime, timesince, nonbreakable_spaces))

    def get_object_id(self, datum):
        return '%s-%s' % (datum['client'], datum['check'])

    class Meta:
        name = "events"
        verbose_name = _("Current Events")
        row_actions = (EventDetail, ResolveEvent, SilenceCheck, SilenceClient)
        table_actions = (FullScreenView, )

class FullScreenSensuEventsTable(tables.DataTable):
    client = tables.Column('client', verbose_name=_("Client"))
    check = tables.Column('check', verbose_name=_("Check"))
    output = tables.Column('output', verbose_name=_("Output"), truncate=100)
    status = tables.Column('status', verbose_name=_("Status"), classes=('status_column',), hidden=True)
    issued = tables.Column('issued', verbose_name=_("Last occurence"), filters=(timestamp_to_datetime, timesince, nonbreakable_spaces))

    def get_object_id(self, datum):
        return '%s-%s' % (datum['client'], datum['check'])


    class Meta:
        name = "events"
        verbose_name = _("Current Events")