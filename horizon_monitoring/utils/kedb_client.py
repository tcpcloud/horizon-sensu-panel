
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

    def check_detail(self, error):
        url = '%s/known-errors/%s' % (self.api, error)
        response = requests.get(url)
        return response.json()

    def error_create(self, error, data):
        payload = data
        url = '%s/known-errors' % self.api
        response = requests.put(url, data=json.dumps(payload))
        return response.json()

    def error_update(self, error, data):
        payload = data
        url = '%s/known-errors/%s' % (self.api, error)
        response = requests.post(url, data=json.dumps(payload))
        return response.json()

    def error_delete(self, error):
        url = '%s/known-errors/%s' % (self.api, error)
        response = requests.get(url)
        return response.json()

kedb_api = Kedb()
