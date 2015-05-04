# -*- coding: UTF-8 -*-
from django.core import urlresolvers
from django.template.defaultfilters import timesince
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from horizon import tables
from horizon import forms
from horizon import exceptions
from horizon import messages
from django import forms as django_forms
from django.db.models.fields import BLANK_CHOICE_DASH
from django.conf import settings
from horizon_monitoring.api import kedb_api

ENGINE_CHOICES = (
    ("salt", u"Salt call"),
    ("jenkins", u"Jenkins job"),
    ("misc", u"Misc"),
)


class WorkaroundDetailForm(django_forms.Form):

    description = forms.CharField(
        label=u"Description", required=True, widget=forms.Textarea)
    action = forms.CharField(
        label=u"Action", required=False, widget=forms.Textarea)
    known_error = forms.CharField(label=u"Known error", required=True)
    engine = forms.ChoiceField(
        required=True, initial='salt', choices=ENGINE_CHOICES)

    def __init__(self, *args, **kwargs):
        super(WorkaroundDetailForm, self).__init__(*args, **kwargs)

    class Meta:
        name = "workarounds"
        verbose_name = _("WorkaroundsFormSet")


class WorkaroundCreateForm(forms.SelfHandlingForm):

    description = forms.CharField(
        label=u"Description", required=True, widget=forms.Textarea)
    action = forms.CharField(
        label=u"Action", required=False, widget=forms.Textarea)
    known_error = forms.CharField(label=u"Known error", required=True)
    engine = forms.ChoiceField(
        required=True, initial='salt', choices=ENGINE_CHOICES)

    def __init__(self, *args, **kwargs):
        super(WorkaroundCreateForm, self).__init__(*args, **kwargs)

    def handle(self, request, data):

        try:
            response = kedb_api.workaround_create(data)
            messages.success(request, _('Workaround Created.'))
        except Exception:
            redirect = urlresolvers.reverse(
                'horizon:monitoring:workarounds:index')
            exceptions.handle(
                request, _(u"Unable to create workaround."), redirect=redirect)

        return True

    class Meta:
        name = "workarounds"
        verbose_name = _("WorkaroundsFormSet")


class WorkaroundUpdateForm(WorkaroundCreateForm):

    id = forms.CharField(label=u"id", required=True, widget=forms.HiddenInput)

    def handle(self, request, data):

        try:
            id = data["id"]
            data.pop("id")
            response = kedb_api.workaround_update(id, data)
            messages.success(
                request, _('Update workaround %s.') % response.get("id"))
        except Exception:
            redirect = urlresolvers.reverse(
                'horizon:monitoring:workarounds:index')
            exceptions.handle(
                request, _("Unable to create workaround."), redirect=redirect)

        return True

    class Meta:
        name = "workarounds"
        verbose_name = _("Workaround update")
