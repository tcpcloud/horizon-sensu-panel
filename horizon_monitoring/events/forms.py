
from django.core.urlresolvers import reverse
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_variables

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon.utils import validators

from horizon_monitoring.utils.sensu_client import sensu_api

class ResolveEventForm(forms.SelfHandlingForm):
    client = forms.CharField(widget=forms.HiddenInput())
    check = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, request, *args, **kwargs):
        super(ResolveEventForm, self).__init__(request, *args, **kwargs)
        self.fields['client'].initial = kwargs.get('initial', {}).get('client')
        self.fields['check'].initial = kwargs.get('initial', {}).get('check')

    def clean(self):
        cleaned_data = super(ResolveEventForm, self).clean()
        return cleaned_data

    # @sensitive_variables('data', 'password')
    def handle(self, request, data):
        client = data.get('client')
        check = data.get('check')

        try:
            response = sensu_api.event_resolve(check, client)
            messages.success(request, _('Resolving event %s.') % response)
        except Exception:
            redirect = reverse('horizon:monitoring:events:index')
            exceptions.handle(request, _("Unable to resolve event."), redirect=redirect)

        return True

class RecheckEventForm(forms.SelfHandlingForm):
    client = forms.CharField(widget=forms.HiddenInput())
    check = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, request, *args, **kwargs):
        super(RecheckEventForm, self).__init__(request, *args, **kwargs)
        self.fields['client'].initial = kwargs.get('initial', {}).get('client')
        self.fields['check'].initial = kwargs.get('initial', {}).get('check')

    def clean(self):
        cleaned_data = super(RecheckEventForm, self).clean()
        return cleaned_data

    def handle(self, request, data):
        client = data.get('client')
        check = data.get('check')

        try:
            response = sensu_api.event_recheck(check, client)
            messages.success(request, _('Rechecking event %s.') % response)
        except Exception:
            redirect = reverse('horizon:monitoring:events:index')
            exceptions.handle(request, _("Unable to recheck event."), redirect=redirect)

        return True

class SilenceCheckForm(forms.SelfHandlingForm):
    client = forms.CharField(widget=forms.HiddenInput())
    check = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, request, *args, **kwargs):
        super(SilenceCheckForm, self).__init__(request, *args, **kwargs)
        self.fields['client'].initial = kwargs.get('initial', {}).get('client')
        self.fields['check'].initial = kwargs.get('initial', {}).get('check')

    def clean(self):
        cleaned_data = super(SilenceCheckForm, self).clean()
        return cleaned_data

    def handle(self, request, data):
        client = data.get('client')
        check = data.get('check')

        try:
            response = sensu_api.check_silence(check, client)
            messages.success(request, _('Silence check event %s.') % response)
        except Exception:
            redirect = reverse('horizon:monitoring:events:index')
            exceptions.handle(request, _("Silence check."), redirect=redirect)
        return True
