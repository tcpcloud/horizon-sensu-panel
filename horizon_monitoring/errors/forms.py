# -*- coding: UTF-8 -*-
from django.core import urlresolvers
from django.template.defaultfilters import timesince
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from horizon import tables
from horizon import forms
from django.db.models.fields import BLANK_CHOICE_DASH
from django.conf import settings

LEVEL_CHOICES = (
    ("level1", u"level 1"),
    ("level2", u"level 2"),
)

SEVERITY_CHOICES = (
    ("low", u"low"),
    ("medium", u"medium"),
    ("high", u"high"),
)

class ErrorDetailForm(forms.SelfHandlingForm):

    name = forms.CharField(label=u"Name", required=True)
    description = forms.CharField(label=u"Description", widget=forms.Textarea)

    check = forms.CharField(label=u"Sensu check", max_length=255, required=True)
    output_pattern = forms.CharField(label=u"Output pattern", required=False, widget=forms.Textarea)
    level = forms.ChoiceField(label=u"Level", required=True, choices=LEVEL_CHOICES, initial='level1')
    severity = forms.ChoiceField(label=u"Level", required=True, choices=SEVERITY_CHOICES, initial='medium')


    def __init__(self, *args, **kwargs):
        super(ErrorDetailForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['name','level', 'severity', 'description', 'check', 'output_pattern',]

    def handle(self, request, data):
        pass

class ErrorCreateForm(ErrorDetailForm):

    def __init__(self, *args, **kwargs):
        super(ErrorCreateForm, self).__init__(*args, **kwargs)

    def handle(self, request, data):
        pass