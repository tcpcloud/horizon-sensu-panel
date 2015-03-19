# -*- coding: UTF-8 -*-

from horizon_monitoring.utils.kedb_client import KedbManager


class Manager(KedbManager):

    def all(self, *args, **kwargs):
        return self.request('/known-errors')

    def get(self, id):
        return self.update(id)

    def update(self, error, data=None):
        url = '/known-errors/%s/' % (error)
        if not data:
            return self.request(url)
        return self.request(url, "PUT", data)

    def create(self, data, request=None):
        url = '/known-errors/'
        return self.request(url, "POST", data, request)

    def delete(self, request, error):
        url = '/known-errors/%s/' % (error)
        return self.request(url, "DELETE", {}, request)
