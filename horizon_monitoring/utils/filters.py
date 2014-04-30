
from django.utils.safestring import SafeString

from datetime import datetime

def timestamp_to_datetime(value):
    return datetime.fromtimestamp(value)

def nonbreakable_spaces(value):
    return SafeString(value.replace(' ', '&nbsp;'))

def join_list_with_comma(value):
    return ', '.join(value)

def join_list_with_newline(value):
    return SafeString('<br />'.join(value))
