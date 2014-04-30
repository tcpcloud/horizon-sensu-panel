
import requests
import json
import logging

from django.conf import settings

log = logging.getLogger('utils.kedb')

class Kedb(object):

    host = settings.KEDB_HOST
    port = settings.KEDB_PORT

    def __init__(self):
        pass

    def request(self, path):
        request = requests.get('%s%s' % (self.api, path))
        return request.json()

    @property
    def api(self):
        return 'http://%s:%s' % (self.host, self.port)

    @property
    def error_list(self):
        return self.request('/api/known-errors')

kedb_api = Kedb()
