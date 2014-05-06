
from django.core.urlresolvers import reverse
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_variables

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon.utils import validators

from horizon_monitoring.utils.sensu_client import sensu_api

class DeleteStashForm(forms.SelfHandlingForm):
    path = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, request, *args, **kwargs):
        super(DeleteStashForm, self).__init__(request, *args, **kwargs)
        self.fields['path'].initial = kwargs.get('initial', {}).get('path')

    def clean(self):
        cleaned_data = super(DeleteStashForm, self).clean()
        return cleaned_data

    def handle(self, request, data):
        path = data.get('path')

        try:
            response = sensu_api.stash_delete(path)
            messages.success(request, _('Delete stash %s.') % response)
        except Exception:
            redirect = reverse('horizon:monitoring:events:index')
            exceptions.handle(request, _("Unable to delete stash."), redirect=redirect)

        return True
