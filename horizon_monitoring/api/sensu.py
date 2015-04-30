
import logging

import requests
from django.conf import settings
from horizon import messages
from .base import ClientBase
from horizon_monitoring.dashboard import include_kedb
from .kedb import Kedb

log = logging.getLogger('utils.sensu')


if include_kedb:
    kedb_api = Kedb()


class Sensu(ClientBase):

    host = getattr(settings, 'SENSU_HOST', 'localhost')
    port = getattr(settings, 'SENSU_PORT', 4567)

    api_prefix = ""

    def set_sensu_api(self, config):
        self.host = config.get('host', 'localhost')
        self.port = config.get('port', 4567)
        return True

    @property
    def check_list(self):
        return self.request('/checks')

    @property
    def aggregates(self):
        return self.request('/aggregates')

    def aggregate_check(self, check, client=None):
        if client:
            url = '/aggregates/{0}/{1}'.format(client, check)
        else:
            url = '/aggregates/{0}'.format(check)
        return self.request(url)

    def check_detail(self, check):
        url = '%s/checks/%s' % (self.api, check)
        response = requests.get(url)
        return response.json()

    def silence(self, payload):
        url = '/stashes'
        return self.request(url, "POST", payload)

    def check_request(self, check, subscibers):
        payload = {"subscibers": subscibers, "check": check}
        url = '/request'
        return self.request(url, "POST", payload)

    def event_resolve(self, check, client):
        payload = {"client": client, "check": check}
        return self.request('/events/resolve', "POST", payload)

    @property
    def stash_list(self):
        return self.request('/stashes')

    def stash_delete(self, path):
        url = '%s/stashes/%s' % (self.api, path)
        response = requests.delete(url)
        return response

    @property
    def client_list(self):
        return self.request('/clients')

    def event_list(self, request=None):
        events = self.request('/events')
        stashes = self.request('/stashes')
        if include_kedb:
            try:
                events = kedb_api.event_list(events)
            except requests.exceptions.ConnectionError:
                if request:
                    messages.error(request, "KEDB API is down !")
        stash_map = []
        for stash in stashes:
            stash_map.append(stash['path'])
        for event in events:
            try:
                if 'silence/%s/%s' % (event['client']['name'],
                                      event['check']['name']) in stash_map:
                    event['silenced'] = True
                elif 'silence/%s' % event['client'] in stash_map:
                    event['silenced'] = True
                else:
                    event['silenced'] = False
            except Exception:
                event['silenced'] = False
            if event['check']['status'] == 3:
                event['status'] = 0
        return sorted(sorted(events, key=lambda x: x['client']['name'],
                             reverse=False),
                      key=lambda x: x['check']['status'], reverse=True)
        # return events

    def event_detail(self, check, client):
        url = '%s/events/%s/%s' % (self.api, client, check)
        response = requests.get(url)
        return response.json()

    def event_recheck(self, check, client):
        check_obj = self.check_detail(check)
        return self.check_request(check, check_obj['subscribers'])

    @property
    def service_status(self):
        return self.request('/info')

sensu_api = Sensu()
