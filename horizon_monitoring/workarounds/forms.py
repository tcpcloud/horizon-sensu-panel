# -*- coding: UTF-8 -*-
from django.core import urlresolvers
from django.template.defaultfilters import timesince
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from horizon import tables
from horizon import forms
from django import forms as django_forms
from django.db.models.fields import BLANK_CHOICE_DASH
from django.conf import settings

class WorkaroundDetailForm(django_forms.Form):
    """base workaround form"""

    #id = forms.CharField(label=u"ID", required=False)
    description = forms.CharField(label=u"description", required=True, widget=forms.Textarea)
    known_error = forms.CharField(label=u"Known error", required=True)

    def __init__(self, *args, **kwargs):
        super(WorkaroundDetailForm, self).__init__(*args, **kwargs)

    def handle(self, request, data):
        pass

    class Meta:
        name = "workarounds"
        verbose_name = _("WorkaroundsFormSet")

class WorkaroundCreateForm(WorkaroundDetailForm):
    """form handle reqiure error id
    """
    def __init__(self, *args, **kwargs):
        super(WorkaroundCreateForm, self).__init__(*args, **kwargs)

    def handle(self, request, data):
        pass