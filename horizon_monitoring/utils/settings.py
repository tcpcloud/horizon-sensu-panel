
"""

common settings for less ugly code

"""

import six
from django.conf import settings
from django.utils.text import slugify

SENSU_MULTI = False

if hasattr(settings, 'SENSU_API') \
        and isinstance(settings.SENSU_API, dict):
    SENSU_MULTI = True

SENSU_API = {}

for dc, config in six.iteritems(getattr(settings, 'SENSU_API', {})):
    SENSU_API[slugify(unicode(dc))] = config
