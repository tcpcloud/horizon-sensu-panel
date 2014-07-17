
import requests 
import json
import logging
from horizon import messages
from django.conf import settings

log = logging.getLogger('utils.kedb')

from horizon_contrib.api.base import BaseClient

class Gitlab(BaseClient):

    host = getattr(settings, "GITLAB_HOST")
    #port = getattr(settings, "GITLAB_PORT")
    private_token = getattr(settings, "GITLAB_TOKEN")
    protocol = "HTTPS"
    verify = False
    api_prefix = "/api/v3"

    def __init__(self):
        pass

    def project_list(self, request=None):
        return self.request('/projects', request=(request or None))

    def deploy_key_list(self, project_id, request=None):
        return self.request('/projects/%s/keys'% project_id)

gitlab_api = Gitlab()
