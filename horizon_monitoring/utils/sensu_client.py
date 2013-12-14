
import requests
import json
import logging

from django.conf import settings

log = logging.getLogger('utils.sensu')

class Sensu(object):

    host = None
    port = None

    def request(self, path):
        return []

    def __init__(self):
        host = settings.SENSU_HOST
        port = settings.SENSU_PORT

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
