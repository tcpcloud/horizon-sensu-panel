
import requests
import json

from django.conf import settings

log = logging.getLogger('utils.sensu')

class Sensu:

    host = settings.SENSU_API.get('host')
    user = settings.SENSU_API.get('user')
    password = settings.SENSU_API.get('password')

    def check_list(self):
        pass
        # return requests request

    def client_list(self):
        pass
        # return requests request

    def event_list(self):
        pass
        # return requests request

