from django.conf import settings
from django.core import urlresolvers
from django.template.defaultfilters import timesince
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from horizon import tables

from horizon_monitoring.utils.filters import timestamp_to_datetime, \
    nonbreakable_spaces, join_list_with_comma, unit_times

from horizon_monitoring.utils.sensu_client import sensu_api

class FullScreenView(tables.LinkAction):
    name = "fullscreen_view"
    verbose_name = _("Fullscreen Mode")
    url = "horizon:monitoring:events:fullscreen_index"
    classes = ("btn")

    def get_link_url(self):
        return urlresolvers.reverse(self.url, args=[])

class RecheckEvent(tables.LinkAction):
    name = "recheck_event"
    verbose_name = _("Recheck Event")
    url = "horizon:monitoring:events:recheck"
    classes = ("ajax-modal", "btn-edit")

    def get_link_url(self, event):
        return urlresolvers.reverse(self.url, args=[event['check'], event['client']])

class ResolveEvent(tables.BatchAction):
    action_present = ("Resolve",)
    action_past = ("Resolved",)
    data_type_singular = _("Event")
    data_type_plural = _("Events")
    name = "resolve_event"
    verbose_name = _("Resolve Event")
    success_url = "horizon:monitoring:events:index"
    classes = ("btn-danger", "btn-delete")

    def action(self, request, event):
        response = sensu_api.event_resolve(event['check'], event['client'])

    def allowed(self, request, instance):
        return True

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

class ErrorCreate(tables.LinkAction):
    """error create
    """
    name = "error_create"
    verbose_name = _("Create Known Error")
    classes = ("ajax-modal", "btn-edit")
    url = "horizon:monitoring:errors:create_check"
    
    def get_link_url(self, datum):
        return urlresolvers.reverse(self.url, kwargs={'check':datum.get("check"), 'client':datum.get("client")})

    def allowed(self, request, instance):
        allowed = False
        try:
            kedb = getattr(settings, "KEDB_HOST", None)
            if kedb:
                allowed = True
        except:
            pass
        finally:
            return allowed

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

    @staticmethod
    def kedb():
        allowed = False
        try:
            kedb = getattr(settings, "KEDB_HOST", None)
            if not kedb:
                allowed = False
        except:
            return allowed

    client = tables.Column('client', verbose_name=_("Client"))
    check = tables.Column('check', verbose_name=_("Check"))
    known_error = tables.Column('known_error', verbose_name=_("Known"))
    error_name = tables.Column('error_name', verbose_name=_("Error name"))
    output = tables.Column('output', verbose_name=_("Output"), truncate=100)
    status = tables.Column('status', verbose_name=_("Status"), classes=('status_column',), hidden=True)
    flapping = tables.Column('flapping', verbose_name=_("Flapping"))
    silenced = tables.Column('silenced', verbose_name=_("Silenced"), classes=('silenced_column',))
    occurrences = tables.Column('occurrences', verbose_name=_("Occured"), filters=(unit_times, ))
    issued = tables.Column('issued', verbose_name=_("Last occurence"), filters=(timestamp_to_datetime, timesince, nonbreakable_spaces))

    def get_object_id(self, datum):
        return '%s-%s' % (datum['client'], datum['check'])

    class Meta:
        name = "events"
        verbose_name = _("Current Events")
        row_actions = (EventDetail, ResolveEvent, RecheckEvent, SilenceCheck, ErrorCreate)# SilenceClient)
        table_actions = (FullScreenView, ResolveEvent )

class FullScreenSensuEventsTable(SensuEventsTable):
    
    def get_object_id(self, datum):
        return '%s-%s' % (datum['client'], datum['check'])

    class Meta:
        name = "events"
        verbose_name = _("Current Events")
        columns = ("client", "check", "output", "status", "silenced", "issued")