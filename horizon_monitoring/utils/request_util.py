    
import requests 
import json
import logging
from horizon import messages
from django.conf import settings

log = logging.getLogger('utils.make_request')

class BaseClient(object):
    """small util class for easy api manipulate

    .. attribute:: host

        Required.

    .. attribute:: port

        Required.

    .. attribute:: api_prefix

        Default to be a string (``api``)

    .. attribute:: protocol

        Optional.

    """

    host = None
    port = None
    protocol = "http"
    api_prefix = "api"

    _req = None
    
    @property
    def req(self):
        if not self._req:
            try:
                self._req = Req(self.host, 
                                self.port,
                                self.protocol,
                                self.api_prefix)
            except Exception, e:
                raise e
        return  self._req

    def request(self, *args, **kwargs):
        if self.req:
            return self.req.make_request(*args, **kwargs)
        else:
            #missing req util instance
            return None

    def __init__(self, *args, **kwargs):
        super(BaseClient, self).__init__(*args, **kwargs)

class Req(object):
    """small util method for simplify create request with handled exceptions
    and debug output

    .. attribute:: host

        Required.

    .. attribute:: port

        Required.

    .. attribute:: api_prefix

        Default to be a string (``api``)

    .. attribute:: protocol

        Optional.

    """

    host = None
    port = None
    port = "HTTP"
    api_prefix = "api"
    
    def __init__(self, host, port, protocol="HTTP", api_prefix="api"):
        try:
            self.host = host
            self.port = port
            self.protocol = protocol
            self.api_prefix = api_prefix
        except Exception, e:
            raise e

    @property
    def api(self, api_prefix="api"):
        return  '{0}://{1}:{2}/{3}'.format(self.protocol.lower(),
                                            self.host, 
                                            self.port,
                                            api_prefix)

    def make_request(self, path, method="GET", params={}, request=None):
        """small util method for simplify create request with handled exceptions
        and debug output

        .. attribute:: path

            Required.

        .. attribute:: method

            The HTTP method for this action. Defaults to ``GET``. Other methods
            may or may not succeed currently.

        .. attribute:: params

            Default to be an empty dictionary (``{}``)

        .. attribute:: request

            Django request object. Provides django messages.
            Useful in debug. 

        """
        log.debug("%s - %s - %s"%(method,path,params))

        if method == "GET":
            response = requests.get('%s%s' % (self.api, path))
        elif method in ["POST", "PUT", "DELETE"]:
            headers = {"Content-Type": "application/json" }
            req = requests.Request(method, '%s%s' % (self.api, path),data=json.dumps(params),headers=headers).prepare()
            response = requests.Session().send(req)

        """delete ok"""
        if response.status_code == 204:
            return True

        if response.status_code in (200, 201):
            return response.json()
        else:
            if request:
                """handle errors"""
                messages.error(request, "%s - %s - %s - %s - %s" % (method, path, params, response.status_code, str(response.text)))
                return {}
            return { 'status_code': response.status_code, 'text': response.text }
