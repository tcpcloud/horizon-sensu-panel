
import requests
import json
import logging
from horizon import messages
from django.conf import settings

log = logging.getLogger('utils.kedb')

from horizon_contrib.api import ClientBase


class Kedb(ClientBase):

    def __init__(self):
        self.host = getattr(settings, "KEDB_HOST", None)
        self.port = getattr(settings, "KEDB_PORT", None)

    @property
    def workaround_list(self):
        return self.request('/workarounds')

    @property
    def error_list(self):
        return self.request('/known-errors')

    def event_list(self, events):
        url = '/events/'
        payload = {"events": events}
        return self.request(url, "POST", payload)

    def event_detail(self, event):
        url = '/events/detail/'
        payload = {"event": event}
        return self.request(url, "POST", payload)

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
        return self.request(url, "POST", workaround)

    def error_update(self, error, data=None):
        url = '/known-errors/%s/' % (error)
        if not data:
            return self.request(url)
        return self.request(url, "PUT", data)

    def error_create(self, data, request=None):
        url = '/known-errors/'
        return self.request(url, "POST", data, request)

    def error_delete(self, request, error):
        url = '/known-errors/%s/' % (error)
        return self.request(url, "DELETE", {}, request)

kedb_api = Kedb()


class KedbManager(Kedb):

    pass
