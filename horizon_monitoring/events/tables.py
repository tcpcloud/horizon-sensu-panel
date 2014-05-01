
from django.utils.translation import ugettext_lazy as _
from horizon import tables

from django.template.defaultfilters import timesince
from horizon_monitoring.utils.filters import timestamp_to_datetime, nonbreakable_spaces, join_list_with_comma

class ResolveEvent(tables.LinkAction):
    name = "resolve_event"  
    verbose_name = _("Resolve")
    classes = ("btn-edit")

    def get_link_url(self, datum):
        #base_url = reverse(self.url, datum['id'])
        return '../detail/%s/' % datum['client']

class EditInstance(tables.LinkAction):
    name = "event_detail"
    verbose_name = _("Details")
    url = "horizon_monitoring:project:instances:update"
    classes = ("ajax-modal", "btn-edit")


    def get_link_url(self, project):
        return self._get_link_url(project, 'instance_info')

    def _get_link_url(self, project, step_slug):
        base_url = urlresolvers.reverse(self.url, args=[project.id])
        param = urlencode({"step": step_slug})
        return "?".join([base_url, param])

    def allowed(self, request, instance):
        return True

class SilenceCheck(tables.LinkAction):
    name = "silence_check"  
    verbose_name = _("Silence Check")
    classes = ("btn")

    def get_link_url(self, datum):
        #base_url = reverse(self.url, datum['id'])
        return '../detail/%s/' % datum['client']

class SilenceClient(tables.LinkAction):
    name = "silence_client"  
    verbose_name = _("Silence Client")
    classes = ("btn")

    def get_link_url(self, datum):
        #base_url = reverse(self.url, datum['id'])
        return '../detail/%s/' % datum['client']


class SensuEventsTable(tables.DataTable):
    client = tables.Column('client', verbose_name=_("Client"))
    check = tables.Column('check', verbose_name=_("Check"))
    occurrences = tables.Column('occurrences', verbose_name=_("Occurences"))
    output = tables.Column('output', verbose_name=_("Output"))
    status = tables.Column('status', verbose_name=_("Status"), classes=('status_column',))
    flapping = tables.Column('flapping', verbose_name=_("Flapping"))
    issued = tables.Column('issued', verbose_name=_("Last Occurences"), filters=(timestamp_to_datetime, timesince, nonbreakable_spaces))

    def get_object_id(self, datum):
        return '%s-%s' % (datum['client'], datum['check'])

    def get_object_id(self, datum):
        return '%s-%s' % (datum['client'], datum['check'])

    class Meta:
        name = "events"
        verbose_name = _("Current Events")
        row_actions = (ResolveEvent, SilenceCheck, SilenceClient)
