
import requests
import json
import logging

from django.conf import settings

log = logging.getLogger('utils.sensu')

class Sensu(object):

    host = settings.SENSU_HOST
    port = settings.SENSU_PORT

    def __init__(self):
        pass

    def request(self, path):
        request = requests.get('%s%s' % (self.api, path))
        return request.json()

    @property
    def api(self):
        return 'http://%s:%s' % (self.host, self.port)

    @property
    def check_list(self):
        return self.request('/checks')

    def check_request(self, check, subscibers):
        payload = { "subscibers": subscibers, "check": check }
        url = '%s/request' % self.api
        response = requests.post(url, data=json.dumps(payload))
        return response

    @property
    def client_list(self):
        return self.request('/clients')

    @property
    def event_list(self):
        events = self.request('/events')
        for event in events:
            if event['status'] == 3:
                event['status'] = 0
        return sorted(sorted(events, key=lambda x: x['client'], reverse=False), key=lambda x: x['status'], reverse=True)
        #return events

    def event_detail(self, check, client):
        url = '%s/events/%s/%s' % (self.api, client, check)
        response = requests.get(url)
        return response.json()

    def event_resolve(self, check, client):
        payload = { "client": client, "check": check }
        url = '%s/resolve' % self.api
        response = requests.post(url, data=json.dumps(payload))
        return response

    @property
    def service_status(self):
        return self.request('/info')

sensu_api = Sensu()
