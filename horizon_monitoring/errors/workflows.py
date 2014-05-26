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
from .tables import KedbErrorsFormsetTable, WorkaroundsFormSet
from openstack_dashboard import api
from horizon_monitoring.utils.kedb_client import kedb_api

from .const import LEVEL_CHOICES, SEVERITY_CHOICES, OWNERSHIP_CHOICES

class CreateErrorAction(workflows.Action):

    id = forms.CharField(widget=forms.widgets.HiddenInput)
    name = forms.CharField(label=u"Name", required=True)
    description = forms.CharField(label=u"Description", widget=forms.Textarea)
    check = forms.CharField(label=u"Sensu check", max_length=255, required=True)
    output_pattern = forms.CharField(label=u"Output pattern", required=False, widget=forms.Textarea)
    level = forms.ChoiceField(label=u"Level", required=True, choices=LEVEL_CHOICES, initial='level1')
    severity = forms.ChoiceField(label=u"Severity", required=True, choices=SEVERITY_CHOICES, initial='medium')
    ownership = forms.ChoiceField(required=True, initial='cloudlab', choices=OWNERSHIP_CHOICES)

    class Meta:
        name = _("Error Info")
        help_text = _("From here you can update a error.")
    def clean(self):
        cleaned_data = super(CreateErrorAction, self).clean()
        return cleaned_data

    def cleaned_data(self):
        return self.clean()

class CreateErrorInfo(workflows.Step):
    action_class = CreateErrorAction
    contributes = ("name",
                   "description",
                   "check",
                   "output_pattern",
                   "level",
                   "severity",
                   "ownership")

class UpdateErrorWorkaroundsAction(workflows.Action):

    def __init__(self, request, *args, **kwargs):
        super(UpdateErrorWorkaroundsAction, self).__init__(request,
                                                       *args,
                                                       **kwargs)
        err_msg = _('Unable to retrieve workarounds list. '
                    'Please try again later.')
  
    def cleaned_data(self):
        return self.clean()

    class Meta:
        name = _("Error Workarounds")
        slug = "update_error_workaounds"

class UpdateErrorAction(CreateErrorAction):

    class Meta:
        name = _("Error detail")
        slug = 'update_info'
        help_text = _("From here you can edit the error details.")

    def clean(self):
        cleaned_data = super(UpdateErrorAction, self).clean()
        return cleaned_data

class UpdateErrorInfo(workflows.Step):
    action_class = UpdateErrorAction
    depends_on = ("id",)
    contributes = ("id",
                   "name",
                   "description",
                   "check",
                   "output_pattern",
                   "level",
                   "severity",
                   "ownership")

class UpdateErrorWorkarounds(workflows.Step):
    action_class = UpdateErrorWorkaroundsAction
    help_text = _("You can control access to this flavor by moving projects "
                  "from the left column to the right column. Only projects "
                  "in the right column can use the flavor. If there are no "
                  "projects in the right column, all projects can use the "
                  "flavor.")
    no_available_text = _("No workarounds found.")

    template_name = "horizon_monitoring/errors/_update.html"
    depends_on = ("id", )
    contributes = ("workarounds",)

    def render(self):
        """Renders the step."""
        request = self.workflow.request
        step_template = template.loader.get_template(self.template_name)
        data = self.workflow.context['workarounds']
        kedb = KedbErrorsFormsetTable(request=request, data=data)
        extra_context = {"form": self.action,
                         "step": self,
                         "workarounds_table": kedb}
        context = template.RequestContext(request, extra_context)
        return step_template.render(context)

class UpdateError(workflows.Workflow):
    slug = "update_error"
    name = _("Edit Error")
    finalize_button_name = _("Save")
    success_message = _('Modified error "%s".')
    failure_message = _('Unable to modify error "%s".')
    success_url = "horizon:monitoring:errors:index"
    #steps = (UpdateErrorWorkarounds,)
    default_steps = [UpdateErrorInfo, UpdateErrorWorkarounds]

    def format_status_message(self, message):
        return message % self.context['name']

    def handle(self, request, data):
        if data["id"]:
            pass
        messages.debug(request, data["id"])
        """
        formset = WorkaroundsFormSet(request.POST, prefix="workarounds")
        workarounds = []
        for form in formset.forms:
            if form.is_valid():
                workarounds.append(form.cleaned_data)       
        """
        error = kedb_api.error_update(error=data["id"])
        data["workarounds"] = error.get("workarounds")
        result = kedb_api.error_update(error=data["id"], data=data)
        messages.info(request, result.get("text"))
        return False #urlresolvers.reverse(self.success_url, args=[])
