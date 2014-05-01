
from django.utils.translation import ugettext_lazy as _
from horizon import tables

from django.template.defaultfilters import timesince
from horizon_monitoring.utils.filters import timestamp_to_datetime, nonbreakable_spaces, join_list_with_comma

class ResolveEvent(tables.LinkAction):
    name = "resolve_event"  
    verbose_name = _("Resolve")
    classes = ("btn")

    def get_link_url(self, datum):
        #base_url = reverse(self.url, datum['id'])
        return '../detail/%s/' % datum['client']

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
    status = tables.Column('status', verbose_name=_("Status"))
    flapping = tables.Column('flapping', verbose_name=_("Flapping"))
    issued = tables.Column('issued', verbose_name=_("Last Occurences"), filters=(timestamp_to_datetime, timesince, nonbreakable_spaces))

    def get_object_id(self, datum):
        return '%s-%s' % (datum['client'], datum['check'])

    def get_object_id(self, datum):
        return '%s-%s' % (datum['client'], datum['check'])

    class Meta:
        name = "events"
        verbose_name = _("Events")
        row_actions = (ResolveEvent, SilenceCheck, SilenceClient)
