
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

    @property
    def client_list(self):
        return self.request('/clients')

    @property
    def event_list(self):
        return self.request('/events')

sensu_api = Sensu()
