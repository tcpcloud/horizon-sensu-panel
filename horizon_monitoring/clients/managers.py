# -*- coding: UTF-8 -*-

from horizon_monitoring.utils.sensu_client import SensuManager


class CheckManager(SensuManager):

    def all(self, *args, **kwargs):
        return self.request('/checks')

    def get(self, check):
        url = '%s/checks/%s' % (self.api, check)
        return self.request.get(url)

    def silence(self, payload):
        url = '/stashes'
        return self.request(url, "POST", payload)

    def request_check(self, check, subscibers):
        payload = {"subscibers": subscibers, "check": check}
        url = '/request'
        return self.request(url, "POST", payload)
