
import requests
import json
import logging

from django.conf import settings

log = logging.getLogger('utils.sensu')

class Sensu:

    host = settings.SENSU_HOST
    port = settings.SENSU_PORT
    user = settings.SENSU_USER
    password = settings.SENSU_PASSWORD

    def check_list(self):
        pass
        # return requests request

    def client_list(self):
        pass
        # return requests request

    def event_list(self):
        pass
        # return requests request

