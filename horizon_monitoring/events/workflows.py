# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from django.utils.translation import ugettext_lazy as _
from django.core import urlresolvers

from django import template
from horizon import exceptions
from horizon import forms
from horizon import workflows
from horizon import messages
from horizon_monitoring.workarounds.tables import WorkaroundTable
from horizon_monitoring.utils.kedb_client import kedb_api

from horizon_monitoring.errors.const import LEVEL_CHOICES, SEVERITY_CHOICES, OWNERSHIP_CHOICES

class DetailEventAction(workflows.Action):

    id = forms.CharField(widget=forms.widgets.HiddenInput)
    client = forms.CharField(required=False)
    check = forms.CharField(required=False)
    output = forms.CharField(label='Output')
    status = forms.CharField(label='Status')
    flapping = forms.CharField(label='Flapping')
    silenced = forms.CharField(label='Silenced')
    occurrences = forms.CharField(label='Occurrences')
    issued =  forms.CharField(label='Issued')

    #errors field
    error_id = forms.CharField(widget=forms.widgets.HiddenInput)
    error_name = forms.CharField(label=u"Name", required=True)
    description = forms.CharField(label=u"Description", widget=forms.Textarea)
    output_pattern = forms.CharField(label=u"Output pattern", required=False, widget=forms.Textarea)
    level = forms.ChoiceField(label=u"Level", required=True, choices=LEVEL_CHOICES)
    severity = forms.ChoiceField(label=u"Severity", required=True, choices=SEVERITY_CHOICES)
    #ownership = forms.ChoiceField(required=True, initial='cloudlab', choices=OWNERSHIP_CHOICES)

    class Meta:
        name = _("Event Info")
        help_text = _("From here you can update a error.")

    def clean(self):
        cleaned_data = super(DetailEventAction, self).clean()
        return cleaned_data

    def cleaned_data(self):
        return self.clean()

class DetailEventInfo(workflows.Step):
    action_class = DetailEventAction
    contributes = ( #event fields
                   "id",
                   "client",
                   "check",
                   "output",
                   "status",
                   "flapping",
                   "silenced",
                   "occurrences",
                   "issued",
                   #errors fields
                   "error_id",
                   "error_name",
                   "description",
                   "output_pattern",
                   "level",
                   "severity",
                   "ownership")

class DetailErrorWorkaroundsAction(workflows.Action):

    def __init__(self, request, *args, **kwargs):
        super(DetailErrorWorkaroundsAction, self).__init__(request,
                                                       *args,
                                                       **kwargs)
        err_msg = _('Unable to retrieve workarounds list. '
                    'Please try again later.')
  
    def cleaned_data(self):
        return self.clean()

    class Meta:
        name = _("Error Workarounds")
        slug = "update_error_workaounds"

class ErrorWorkaroundsInfo(workflows.Step):
    action_class = DetailErrorWorkaroundsAction
    help_text = _("") #TODO
    no_available_text = _("No workarounds found.")

    template_name = "horizon_monitoring/events/_detail_workarounds.html"
    depends_on = ("error_id",)
    #contributes = ("workarounds",)

    def render(self):
        """Renders the step."""
        request = self.workflow.request
        step_template = template.loader.get_template(self.template_name)
        data = kedb_api.error_update(self.workflow.context['error_id']).get("workarounds", [])
        workarounds_table = WorkaroundTable(request=request, data=data)
        extra_context = {"form": self.action,
                         "step": self,
                         "workarounds_table": workarounds_table}
        context = template.RequestContext(request, extra_context)
        return step_template.render(context)

class DetailEvent(workflows.Workflow):
    slug = "detail_event"
    name = _("Event Detail")
    finalize_button_name = _("Save")
    #success_message = _('"%s".')
    #failure_message = _('Unable to show close dialog"%s".')
    success_url = "horizon:monitoring:events:index"
    default_steps = [DetailEventInfo, ErrorWorkaroundsInfo]

    def format_status_message(self, message):
        return message % self.context['name']

    def handle(self, request, data):
        return True
