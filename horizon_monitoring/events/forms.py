import time

from django.core.urlresolvers import reverse
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_variables

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon.utils import validators

from horizon_monitoring.utils.sensu_client import sensu_api


class EventForm(forms.SelfHandlingForm):
    client = forms.CharField(widget=forms.HiddenInput(), required=False)
    check = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        return cleaned_data

    def handle(self, request, data):
        pass


class SilenceForm(EventForm):
    expire = forms.IntegerField(required=True)
    reason = forms.CharField(widget=forms.Textarea(), required=False)

    def __init__(self, request, *args, **kwargs):
        super(SilenceForm, self).__init__(request, *args, **kwargs)
        self.fields['expire'].initial = 120

    def clean(self):
        cleaned_data = super(SilenceForm, self).clean()
        return cleaned_data

    def handle(self, request, data):
        client = data.get('client', None)
        check = data.get('check', None)
        expire = data.get('expire')
        content = {
            'timestamp': int(time.time()),
            'reason': data.get('reason'),
        }

        payload = {"content": content}

        if check and client:
            payload["path"] = 'silence/%s/%s' % (client, check)
        else:
            payload["path"] = 'silence/%s' % client

        if expire != -1:
            payload["expire"] = expire

        response = sensu_api.silence(payload)
        try:
            messages.success(request, _('Silence check event %s.') % response)
        except Exception:
            redirect = reverse('horizon:monitoring:events:index')
            exceptions.handle(request, _("Silence check."), redirect=redirect)
        return True
