import time

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions, forms, messages
from horizon_monitoring.utils import settings as sensu_settings
from horizon_monitoring.api import sensu_api


class EventForm(forms.SelfHandlingForm):
    client = forms.CharField(widget=forms.HiddenInput(), required=False)
    check = forms.CharField(widget=forms.HiddenInput(), required=False)
    dc = forms.CharField(widget=forms.HiddenInput(), required=False)

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

        dc = data.get('dc', None)
        if dc and sensu_settings.SENSU_MULTI:
            sensu_api.set_sensu_api(sensu_settings.SENSU_API.get(dc))

        response = sensu_api.silence(payload)
        try:
            messages.success(request, _('Silence check event %s.') % response)
        except Exception:
            redirect = reverse('horizon:monitoring:events:index')
            exceptions.handle(request, _("Silence check."), redirect=redirect)
        return True
