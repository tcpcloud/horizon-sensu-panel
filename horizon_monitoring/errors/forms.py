# -*- coding: UTF-8 -*-
from django.core import urlresolvers
from django.template.defaultfilters import timesince
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
#from django import forms as django_forms
from horizon import tables
from horizon import forms
from horizon import exceptions
from horizon import messages
from django.db.models.fields import BLANK_CHOICE_DASH
from django.conf import settings
from .const import LEVEL_CHOICES, SEVERITY_CHOICES, OWNERSHIP_CHOICES
from horizon_monitoring.utils.kedb_client import kedb_api
from horizon_monitoring.utils.sensu_client import sensu_api

"""
class ErrorDetailForm(forms.Form):
    name = forms.CharField(label=u"Name", required=True)
    description = forms.CharField(label=u"Description", widget=forms.Textarea)

    check = forms.CharField(label=u"Sensu check", max_length=255, required=True)
    output_pattern = forms.CharField(label=u"Output pattern", required=False, widget=forms.Textarea)
    level = forms.ChoiceField(label=u"Level", required=True, choices=LEVEL_CHOICES, initial='level1')
    severity = forms.ChoiceField(label=u"Severity", required=True, choices=SEVERITY_CHOICES, initial='medium')

    def __init__(self, *args, **kwargs):
        super(ErrorDetailForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['name','level', 'severity', 'description', 'check', 'output_pattern',]
"""

class ErrorDetailForm(forms.SelfHandlingForm):

    name = forms.CharField(label=u"Name", required=True)
    description = forms.CharField(label=u"Description", widget=forms.Textarea)

    check = forms.CharField(label=u"Sensu check", max_length=255, required=True)
    output_pattern = forms.CharField(label=u"Output pattern", required=False, widget=forms.Textarea)
    level = forms.ChoiceField(label=u"Level", required=True, choices=LEVEL_CHOICES, initial='level1')
    severity = forms.ChoiceField(label=u"Severity", required=True, choices=SEVERITY_CHOICES, initial='medium')
    ownership = forms.ChoiceField(required=True, initial='cloudlab', choices=OWNERSHIP_CHOICES)

    def __init__(self, *args, **kwargs):
        super(ErrorDetailForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['name','level', 'severity', 'description', 'check', 'output_pattern', 'ownership']

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
            messages.success(request, _('Create error %s.') % response.get("name"))
        except Exception:
            redirect = urlresolvers.reverse('horizon:monitoring:errors:index')
            exceptions.handle(request, _("Unable to create error."), redirect=redirect)
        
        return True

class ErrorCheckCreateForm(ErrorDetailForm):
    """mel by jit volat bez sensu checku tak i snim
    """

    resolve = forms.BooleanField(required=True, initial=False, label=u"Resolve check ?")
    #silence = forms.BooleanField(required=True, initial=False, label=u"Silence check ?")

    def __init__(self, *args, **kwargs):
        super(ErrorCheckCreateForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['resolve','name','level', 'severity', 'description', 'check', 'output_pattern', 'ownership']

    def handle(self, request, data):
        
        try:
            response = kedb_api.error_create(data)
            messages.success(request, _('Create error %s.') % response.get("name"))
            
            if data.get("resolve", False):
                try:
                    response = sensu_api.event_resolve(data.get("check"), data.get("client"))
                    messages.success(request, _('Resolving event %s.') % response)
                except Exception, e:
                    messages.error(request, _('In Resolving event %s.') % response)
        
        except Exception:
            redirect = urlresolvers.reverse('horizon:monitoring:errors:index')
            exceptions.handle(request, _("Unable to create error."), redirect=redirect)

        return True