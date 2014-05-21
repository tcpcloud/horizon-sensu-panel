
import requests 
import json
import logging
from horizon import messages
from django.conf import settings

log = logging.getLogger('utils.kedb')

class Kedb(object):

    host = settings.KEDB_HOST
    port = settings.KEDB_PORT

    def __init__(self):
        pass

    def request(self, path, method="GET", params={}, request=None):
        log.debug("%s - %s - %s"%(method,path,params))

        if method == "GET":
            response = requests.get('%s%s' % (self.api, path))
        elif method in ["POST", "PUT", "DELETE"]:
            headers = {"Content-Type": "application/json" }
            req = requests.Request(method, '%s%s' % (self.api, path),data=json.dumps(params),headers=headers).prepare()
            response = requests.Session().send(req)

        if response.status_code in (200, 201, 204):
            return response.json()
        else:
            if request:
                """handle errors"""
                messages.error(request, "%s - %s - %s - %s - %s" % (method, path, params, response.status_code, str(response.text)))
                return {}
            return { 'status_code': response.status_code, 'text': response.text }

    @property
    def api(self):
        return 'http://%s:%s/api' % (self.host, self.port)

    @property
    def workaround_list(self):
        return self.request('/workarounds')

    @property
    def error_list(self):
        return self.request('/known-errors')

    def workaround_update(self, workaround, data=None):
        """zapouzdruje jak detail tak update
        """
        url = '/workarounds/%s/' % (workaround)
        if not data:
            return self.request(url)
        return self.request(url, "PUT", data)

    def workaround_delete(self, workaround):
        url = '/workarounds/%s/' % (workaround)
        return self.request(url, "DELETE", {})

    def workaround_create(self, workaround):
        url = '/workarounds/'
        return self.request(url, "PUT", workaround)

    def error_update(self, error, data=None):
        url = '/known-errors/%s/' % (error)
        if not data:
            return self.request(url)
        return self.request(url, "PUT", data)

    def error_create(self, error, data):
        url = '/known-errors'
        return self.request(url, "PUT", data)

    def error_delete(self, request, error):
        url = '/known-errors/%s/' % (error)
        return self.request(url, "DELETE", {}, request)

kedb_api = Kedb()
