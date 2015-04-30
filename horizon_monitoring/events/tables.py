
from collections import defaultdict
import random
import six
from django.conf import settings
from django.core import urlresolvers
from django.template.defaultfilters import timesince
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from horizon import tables
from horizon_monitoring.templatetags.tables import *

from horizon_monitoring.dashboard import include_kedb
from horizon_monitoring.utils import settings as sensu_settings, FilterAction
from horizon_monitoring.api import kedb_api, sensu_api
from horizon import messages


class FullScreenView(tables.LinkAction):
    name = "fullscreen_view"
    verbose_name = _("Fullscreen Mode")
    url = "horizon:monitoring:events:fullscreen_index"
    classes = ("btn")

    def get_link_url(self):
        return urlresolvers.reverse(self.url, args=[])


class EventAction(tables.BatchAction):

    """base event action"""
    data_type_singular = _("Event")
    data_type_plural = _("Events")

    verbose_name = _("Resolve Event")
    success_url = "horizon:monitoring:events:index"
    classes = ("btn-primary", "btn-danger")

    def get_check_client(self, object_id):
        """returns check, client, and dc if multi
        """
        attrs = object_id.split(" ")
        return attrs[0], attrs[1]

    def set_sensu(self, object_id):
        if sensu_settings.SENSU_MULTI:
            dc = object_id.split(" ")[2]
            sensu_api.set_sensu_api(sensu_settings.SENSU_API.get(dc))

    def resolve(self, request, object_id):
        self.set_sensu(object_id)
        check, client = self.get_check_client(object_id)
        response = sensu_api.event_resolve(check, client)
        messages.info(request, response)

    def action(self, request, object_id):
        pass


class RecheckEvent(EventAction):
    action_present = ("Recheck",)
    action_past = ("Rechecked",)
    name = "recheck_event"
    verbose_name = _("Recheck Event")
    success_url = "horizon:monitoring:events:index"
    classes = ("btn-primary", "btn-danger", "btn-info")

    def action(self, request, object_id):
        self.set_sensu(object_id)
        check, client = self.get_check_client(object_id)
        response = sensu_api.event_recheck(check, client)
        raise Exception(response)
        messages.info(request, response)

    def allowed(self, request, instance):
        return True


class ResolveEvent(EventAction):
    action_present = ("Resolve",)
    action_past = ("Resolved",)
    name = "resolve_event"
    verbose_name = _("Resolve Event")
    success_url = "horizon:monitoring:events:index"
    classes = ("btn-primary", "btn-danger", "btn-success")

    def action(self, request, object_id):
        self.resolve(request, object_id)

    def allowed(self, request, instance):
        return True


class EventDetail(tables.LinkAction):
    name = "event_detail"
    verbose_name = _("Event Detail")
    url = "horizon:monitoring:events:detail"
    classes = ("btn-edit")

    def get_link_url(self, e):
        if sensu_settings.SENSU_MULTI:
            args = [e['check']['name'], e['client']['name'], e['datacenter']]
        else:
            args = [e['check']['name'], e['client']['name']]
        return urlresolvers.reverse(self.url, args=args)

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
        return urlresolvers.reverse(self.url, kwargs={'check': datum.get("check").get('name'), 'client': datum.get("client").get('name')})

    def allowed(self, request, instance):
        allowed = False
        if include_kedb:
            if not instance.get("known_error", False):
                allowed = True
        return allowed


class StashDelete(tables.DeleteAction):
    action_present = ("Delete",)
    action_past = ("Deleted",)
    data_type_singular = _("Stash")
    data_type_plural = _("stashes")
    name = "stash_delete"
    success_url = "horizon:monitoring:events:index"

    def get_check_client(self, object_id):
        check, client = None, None
        client, check = object_id.split(" ")
        return client, check

    def is_client(self, client, check):
        """zjisti jestli jestli je stashlej jenom client/check nebo celej client
        neprisli sme na lepsi reseni
        """
        events = sensu_api.event_list
        stashes = sensu_api.stash_list
        if include_kedb:
            events = kedb_api.event_list(events)
        stash_map = []
        for stash in stashes:
            stash_map.append(stash['path'])
        for event in events:
            if 'silence/%s/%s' % (event['client']['name'], event['check']['name']) in stash_map:
                return False
            elif 'silence/%s' % event['client']['name'] in stash_map:
                return True
        return False

    def delete(self, request, path):
        client, check = self.get_check_client(path)
        _path = "silence/%s" % client
        if not self.is_client(client, check):
            _path = "%s/%s" % (_path, check)
        sensu_api.stash_delete(_path)

    def allowed(self, request, instance):
        if instance.get("silenced", False):
            return True
        return False


class SilenceClient(tables.LinkAction):
    name = "silence_client"
    verbose_name = _("Silence Client")
    url = "horizon:monitoring:events:silence_client"
    classes = ("ajax-modal", "btn-edit")

    def get_link_url(self, e):
        args = [e['client']['name']]
        if sensu_settings.SENSU_MULTI:
            args = [e['client']['name'], e['datacenter']]
        return urlresolvers.reverse(self.url, args=args)


class SilenceCheck(tables.LinkAction):
    name = "silence_client_check"
    verbose_name = _("Silence Check")
    url = "horizon:monitoring:events:silence_client_check"
    classes = ("ajax-modal", "btn")

    def get_link_url(self, e):
        args = [e['client']['name'], e['check']['name']]
        if sensu_settings.SENSU_MULTI:
            args = [e['client']['name'], e['check']['name'], e['datacenter']]
        return urlresolvers.reverse(self.url, args=args)


class EventFilter(tables.FixedFilterAction):

    def get_fixed_buttons(self):
        """generate category buttons
        """
        def make_dict(text, datacenter, icon):
            return dict(text=text, value=datacenter, icon=icon)

        append = []
        for dc, config in six.iteritems(getattr(settings, 'SENSU_API', {})):
            icon = config.get(
                'icon', random.choice(['fa fa-database',
                                       'fa fa-server',
                                       'fa fa-cloud-upload',
                                       'fa fa-cloud-download']))
            append.append(
                make_dict(config.get("name", dc), slugify(unicode(dc)), icon))
        return append + [make_dict(_("All"), "all", "fa fa-cloud")]

    def categorize(self, table, items):
        results = defaultdict(list)

        self.items = items
        # must be reloaded
        for item in items:
            results['all'].append(item)
            results[item['datacenter']].append(item)
        return results


class EventRow(tables.Row):

    def load_cells(self, event=None):
        super(EventRow, self).load_cells(event)
        # Tag the event with the datacenter
        self.classes.append('category-all')
        self.classes.append('category-' + self.datum['datacenter'])

if sensu_settings.SENSU_MULTI:
    FILTER_ACTION = [EventFilter]
    FULL_FILTER_ACTION = [EventFilter]
else:
    FILTER_ACTION = [FilterAction]
    FULL_FILTER_ACTION = []

check_filter = getattr(
    settings, 'SENSU_CHECK_FILTER',
    lambda c: c['name'])


class SensuEventsTable(tables.DataTable):

    def get_error_link(self):
        url = "horizon:monitoring:errors:update"
        error_id = self.get("error_id", None)
        if error_id:
            return urlresolvers.reverse(url, args=(error_id,))
        return ""

    client = tables.Column(
        'client', verbose_name=_("Client"), filters=(lambda c: c['name'],))
    address = tables.Column(
        'client', verbose_name=_("Address"), filters=(lambda c: c['address'],))
    check = tables.Column(
        'check', verbose_name=_("Check"), filters=(check_filter,))

    if include_kedb:
        error_name = tables.Column('error_name', verbose_name=_("Error name"))
    output = tables.Column('check', verbose_name=_(
        "Output"), truncate=180, filters=(lambda c: c['output'],))
    status = tables.Column('status', verbose_name=_(
        "Status"), classes=('status_column',), hidden=True)
    flapping = tables.Column('flapping', verbose_name=_("Flapping"), classes=(
        'silenced_column', 'centered'), filters=(status_image,))
    silenced = tables.Column('silenced', verbose_name=_("Silenced"),
                             classes=('silenced_column', 'centered'), filters=(status_image,))
    occurrences = tables.Column(
        'occurrences', verbose_name=_("Occured"), filters=(unit_times,))
    issued = tables.Column('check', verbose_name=_("Last occurence"),
                           filters=(lambda c: c['issued'], timestamp_to_datetime, timesince, nonbreakable_spaces))

    def get_object_id(self, datum):
        if sensu_settings.SENSU_MULTI:
            return '%s %s %s' % (datum['client']['name'], datum['check']['name'], datum['datacenter'])
        return '%s %s' % (datum['client']['name'], datum['check']['name'])

    def get_object_display(self, datum):
        return '%s %s' % (datum['client']['name'], datum['check']['name'])

    class Meta:
        name = "events"
        verbose_name = _("Current Events")
        row_actions = (EventDetail,
                       ResolveEvent,
                       RecheckEvent,
                       # SilenceCheck,
                       SilenceClient,
                       SilenceCheck,
                       ErrorCreate,
                       StashDelete)
        table_actions = [FullScreenView,
                         ResolveEvent,
                         RecheckEvent] + FILTER_ACTION
        if sensu_settings.SENSU_MULTI:
            row_class = EventRow


class FullScreenSensuEventsTable(SensuEventsTable):

    def get_object_id(self, datum):
        return '%s %s' % (datum['client'], datum['check'])

    class Meta:
        name = "events"
        verbose_name = _("Current Events")
        columns = ("client", "check", "output", "status", "issued")
        table_actions = FULL_FILTER_ACTION
