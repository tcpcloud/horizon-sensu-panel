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

from django import template
from horizon import exceptions
from horizon import forms
from horizon import workflows
from horizon_monitoring.workarounds.tables import WorkaroundTable
from .tables import KedbErrorsFormsetTable
from openstack_dashboard import api
from .const import LEVEL_CHOICES, SEVERITY_CHOICES, OWNERSHIP_CHOICES

class CreateErrorAction(workflows.Action):
    _flavor_id_regex = (r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-'
                        r'[0-9a-fA-F]{4}-[0-9a-fA-F]{12}|[0-9]+|auto$')
  
    name = forms.RegexField(label=_("Name"),
                            max_length=255,
                            regex=r'^[\w\.\- ]+$',
                            error_messages={'invalid': _('Name may only '
                                'contain letters, numbers, underscores, '
                                'periods and hyphens.')})

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

class CreateErrorInfo(workflows.Step):
    action_class = CreateErrorAction
    contributes = ("name",
                   "description",
                   "check",
                   "output_pattern",
                   "level",
                   "severity",
                   "ownership")

class UpdateErrorWorkaroundsAction(workflows.MembershipAction):

    def __init__(self, request, *args, **kwargs):
        super(UpdateErrorWorkaroundsAction, self).__init__(request,
                                                       *args,
                                                       **kwargs)
        err_msg = _('Unable to retrieve workarounds list. '
                    'Please try again later.')

    class Meta:
        name = _("Error Workarounds")
        slug = "update_error_workaounds"

class UpdateErrorWorkarounds(workflows.Step):
    action_class = UpdateErrorWorkaroundsAction
    help_text = _("You can control access to this flavor by moving projects "
                  "from the left column to the right column. Only projects "
                  "in the right column can use the flavor. If there are no "
                  "projects in the right column, all projects can use the "
                  "flavor.")
    no_available_text = _("No workarounds found.")

    template_name = "horizon_monitoring/errors/_update.html"
    depends_on = ("id",)
    contributes = ("error_id",)

    def render(self):
        """Renders the step."""
        request = self.workflow.request
        """mega psycho fuj, budeme delat jakobych to nikdy nenapsal"""
        array = self.workflow.get_absolute_url().split("/")
        error_id = array[-3]
        step_template = template.loader.get_template(self.template_name)
        data_ = kedb_api.error_detail(error_id).get("workarounds")
        kedb = KedbErrorsFormsetTable(request=request, data=data_)
        extra_context = {"form": self.action,
                         "step": self,
                         "workarounds_table": kedb,
                         "formset": WorkaroundsFormSet(initial=data_, prefix="workarounds") }
        context = template.RequestContext(request, extra_context)
        return step_template.render(context)

class CreateFlavor(workflows.Workflow):
    slug = "create_flavor"
    name = _("Create Error")
    finalize_button_name = _("Create Errorr")
    success_message = _('Created new error "%s".')
    failure_message = _('Unable to create error "%s".')
    success_url = "horizon:monitoring:errors:index"
    default_steps = (CreateErrorInfo,
                     UpdateErrorWorkarounds)

    def format_status_message(self, message):
        return message % self.context['name']

    def handle(self, request, data):
        flavor_id = data.get('flavor_id') or 'auto'
        flavor_access = data['flavor_access']
        is_public = not flavor_access

        # Create the flavor
        try:
            self.object = api.nova.flavor_create(request,
                                                 name=data['name'],
                                                 memory=data['memory_mb'],
                                                 vcpu=data['vcpus'],
                                                 disk=data['disk_gb'],
                                                 ephemeral=data['eph_gb'],
                                                 swap=data['swap_mb'],
                                                 flavorid=flavor_id,
                                                 is_public=is_public)
        except Exception:
            exceptions.handle(request, _('Unable to create flavor.'))
            return False

        # Update flavor access if the new flavor is not public
        flavor_id = self.object.id
        for project in flavor_access:
            try:
                api.nova.add_tenant_to_flavor(
                    request, flavor_id, project)
            except Exception:
                exceptions.handle(request,
                    _('Unable to set flavor access for project %s.') % project)
        return True


class UpdateErrorAction(CreateErrorAction):
    error_id = forms.CharField(widget=forms.widgets.HiddenInput)

    class Meta:
        name = _("Error detail")
        slug = 'update_info'
        help_text = _("From here you can edit the error details.")

    def clean(self):
        return self.cleaned_data

class UpdateError(workflows.Step):
    action_class = UpdateErrorAction
    depends_on = ("error_id",)
    contributes = ("error_id",
                   "name",
                   "description",
                   "check",
                   "output_pattern",
                   "level",
                   "severity",
                   "ownership")

from horizon_monitoring.utils.kedb_client import kedb_api

class UpdateError(workflows.Workflow):
    slug = "update_error"
    name = _("Edit Error")
    finalize_button_name = _("Save")
    success_message = _('Modified error "%s".')
    failure_message = _('Unable to modify error "%s".')
    success_url = "horizon:monitoring:errors:index"
    default_steps = (UpdateError,
                     UpdateErrorWorkarounds)

    def format_status_message(self, message):
        return message % self.context['name']

    def handle(self, request, data):

        # Add flavor access if the flavor is not public.
        for project in flavor_projects:
            try:
                api.nova.add_tenant_to_flavor(request, flavor.id, project)
            except Exception:
                exceptions.handle(request, _('Modified flavor information, '
                                             'but unable to modify flavor '
                                             'access.'))
        return True
