
import requests
import json
import logging
from horizon import messages

from django.conf import settings

try:
    from horizon_monitoring.utils.kedb_client import kedb_api
    host = settings.KEDB_HOST
    include_kedb = True
except:
    include_kedb = False

log = logging.getLogger('utils.sensu')

from horizon_monitoring.utils.api_client import BaseClient

class Sensu(BaseClient):

    host = settings.SENSU_HOST
    port = settings.SENSU_PORT
    api_prefix = ""

    def __init__(self):
        pass

    @property
    def check_list(self):
        return self.request('/checks')

    def check_detail(self, check):
        url = '%s/checks/%s' % (self.api, check)
        response = requests.get(url)
        return response.json()

    def silence(self, payload):
        """
        {
          "path": "random_stash",
          "expire": 60,
          "content": {
            "reason": "things are stashy"
          }
        }
        """ 
        url = '/stashes'
        return self.request(url, "POST", payload)

    def check_request(self, check, subscibers):
        payload = { "subscibers": subscibers, "check": check }
        url = '/request'
        return self.request(url, "POST", payload)

    def event_resolve(self, check, client):
        url = '/events/%s/%s' % (client, check)
        return self.request(url, "DELETE")

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
            if 'silence/%s/%s' % (event['client'], event['check']) in stash_map:
                event['silenced'] = True
            elif 'silence/%s'% event['client'] in stash_map:
                event['silenced'] = True
            else:
                event['silenced'] = False
            if event['status'] == 3:
                event['status'] = 0
        return sorted(sorted(events, key=lambda x: x['client'], reverse=False), key=lambda x: x['status'], reverse=True)
        #return events

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
