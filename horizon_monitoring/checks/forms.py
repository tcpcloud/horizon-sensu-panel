
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from horizon_monitoring.api import sensu_api


class RequestCheckForm(forms.SelfHandlingForm):
    subscibers = forms.CharField()
    check = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, request, *args, **kwargs):
        super(RequestCheckForm, self).__init__(request, *args, **kwargs)
        self.fields['check'].initial = kwargs.get('initial', {}).get('check')

    def clean(self):
        cleaned_data = super(RequestCheckForm, self).clean()
        return cleaned_data

    def handle(self, request, data):
        check = data.get('check')
        subscibers = data.get('subscibers').split(',')

        try:
            response = sensu_api.check_request(check, subscibers)
            messages.success(request, _('Requesting check %s.') % response)
        except Exception:
            redirect = reverse('horizon:monitoring:checks:index')
            exceptions.handle(
                request, _("Unable to request check."), redirect=redirect)

        return True
