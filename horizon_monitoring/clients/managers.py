# -*- coding: UTF-8 -*-

from horizon_monitoring.utils.sensu_client import SensuManager


class ClientManager(SensuManager):

    def all(self, *args, **kwargs):
        return self.request('/clients')

    def get(self, check):
        url = '%s/clients/%s' % (self.api, check)
        return self.request.get(url)
