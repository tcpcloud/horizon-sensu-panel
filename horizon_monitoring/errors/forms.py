# -*- coding: UTF-8 -*-
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions, forms, messages
from horizon_monitoring.api import kedb_api

from .const import LEVEL_CHOICES, OWNERSHIP_CHOICES, SEVERITY_CHOICES


class ErrorDetailForm(forms.SelfHandlingForm):

    name = forms.CharField(label=u"Name", required=True)
    description = forms.CharField(label=u"Description", widget=forms.Textarea)

    check = forms.CharField(
        label=u"Sensu check", max_length=255, required=True)
    output_pattern = forms.CharField(
        label=u"Output pattern", required=False, widget=forms.Textarea)
    level = forms.ChoiceField(
        label=u"Level", required=True, choices=LEVEL_CHOICES)
    severity = forms.ChoiceField(
        label=u"Severity", required=True, choices=SEVERITY_CHOICES)
    ownership = forms.ChoiceField(
        required=True, initial='cloudlab', choices=OWNERSHIP_CHOICES)

    def __init__(self, *args, **kwargs):
        super(ErrorDetailForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'name', 'level', 'severity', 'description', 'check', 'output_pattern', 'ownership']

    def handle(self, request, data):
        pass


class ErrorCreateForm(ErrorDetailForm):

    """mel by jit volat bez sensu checku tak i snim
    """

    def __init__(self, *args, **kwargs):
        super(ErrorCreateForm, self).__init__(*args, **kwargs)

    def handle(self, request, data):

        try:
            response = kedb_api.error_create(data)
            messages.success(
                request, _('Create error %s.') % response.get("name"))
        except Exception:
            redirect = urlresolvers.reverse('horizon:monitoring:errors:index')
            exceptions.handle(
                request, _("Unable to create error."), redirect=redirect)

        return True


class ErrorCheckCreateForm(ErrorDetailForm):

    """mel by jit volat bez sensu checku tak i snim
    """

    #resolve = forms.BooleanField(required=True, initial=False, label=u"Resolve check ?")
    #silence = forms.BooleanField(required=True, initial=False, label=u"Silence check ?")

    def __init__(self, *args, **kwargs):
        super(ErrorCheckCreateForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'name', 'level', 'severity', 'description', 'check', 'output_pattern', 'ownership']

    def handle(self, request, data):

        try:
            response = kedb_api.error_create(data)
            messages.success(
                request, _('Create error %s.') % response.get("name"))

            """       
            if data.get("resolve", False):
                try:
                    response = sensu_api.event_resolve(data.get("check"), data.get("client"))
                    messages.success(request, _('Resolving event %s.') % response)
                except Exception, e:
                    messages.error(request, _('In Resolving event %s.') % response)
            """

        except Exception:
            redirect = urlresolvers.reverse('horizon:monitoring:errors:index')
            exceptions.handle(
                request, _("Unable to create kwown error."), redirect=redirect)

        return True


class UpdateErrorForm(ErrorDetailForm):

    id = forms.CharField(widget=forms.widgets.HiddenInput)

    class Meta:
        name = _("Error Info")
        help_text = _("From here you can update a error.")

    def __init__(self, *args, **kwargs):
        super(ErrorDetailForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'name', 'level', 'severity', 'description', 'check', 'output_pattern', 'ownership', 'id']

    def handle(self, request, data):

        try:
            error_id = data["id"]
            data.pop("id")
            response = kedb_api.error_update(error_id, data)
            messages.success(
                request, _('Update error %s.') % response.get("name"))

        except Exception:
            redirect = urlresolvers.reverse('horizon:monitoring:errors:index')
            exceptions.handle(
                request, _("Unable to create kwown error."), redirect=redirect)

        return True
