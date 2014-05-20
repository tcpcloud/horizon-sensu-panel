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

from horizon import exceptions
from horizon import forms
from horizon import workflows

from openstack_dashboard import api
from horizon_monitoring.utils.kedb_client import kedb_api

LEVEL_CHOICES = (
    ("level1", u"level 1"),
    ("level2", u"level 2"),
)

SEVERITY_CHOICES = (
    ("low", u"low"),
    ("medium", u"medium"),
    ("high", u"high"),
)

class CreateErrorInfoAction(workflows.Action):
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

    class Meta:
        name = _("Error Info")
        help_text = _("From here you can update a "
                      "error to organize workarounds.")

    def clean(self):
        cleaned_data = super(CreateErrorInfoAction, self).clean()
        return cleaned_data

class CreateErrorInfo(workflows.Step):
    action_class = CreateErrorInfoAction
    contributes = ("error_id",
                   "name",
                   "description",
                   "check",
                   "output_pattern",
                   "level",
                   "severity")


class UpdateFlavorAccessAction(workflows.MembershipAction):
    def __init__(self, request, *args, **kwargs):
        super(UpdateFlavorAccessAction, self).__init__(request,
                                                       *args,
                                                       **kwargs)
        err_msg = _('Unable to retrieve workarounds list. '
                    'Please try again later.')
        context = args[0]

        default_role_field_name = self.get_default_role_field_name()
        self.fields[default_role_field_name] = forms.CharField(required=False)
        self.fields[default_role_field_name].initial = 'member'

        field_name = self.get_member_field_name('member')
        self.fields[field_name] = forms.MultipleChoiceField(required=False)

        # Get list of available projects.
        workarounds = []
        error_id = context.get('error_id')
        try:
            workarounds = kedb_api.error_detail(error=error_id).get("workarounds")
            has_more = True
        except Exception:
            exceptions.handle(request, err_msg)
        projects_list = [(workaround.get("id"), workaround.get("description"))
                         for workaround in workarounds]

        self.fields[field_name].choices = projects_list

        # If we have a POST from the CreateFlavor workflow, the flavor id
        # isn't an existing flavor. For the UpdateFlavor case, we don't care
        # about the access list for the current flavor anymore as we're about
        # to replace it.
        if request.method == 'POST':
            return

        # Get list of flavor projects if the flavor is not public.
        flavor_access = []
        try:
            if error_id:
                error = kedb_api.error_detail(error_id)
                flavor_access = error.get("workarounds")
        except Exception:
            exceptions.handle(request, err_msg)

        self.fields[field_name].initial = flavor_access

    class Meta:
        name = _("Flavor Access")
        slug = "update_flavor_access"


class UpdateFlavorAccess(workflows.UpdateMembersStep):
    action_class = UpdateFlavorAccessAction
    help_text = _("You can control access to this flavor by moving projects "
                  "from the left column to the right column. Only projects "
                  "in the right column can use the flavor. If there are no "
                  "projects in the right column, all projects can use the "
                  "flavor.")
    available_list_title = _("All Projects")
    members_list_title = _("Selected Projects")
    no_available_text = _("No projects found.")
    no_members_text = _("No projects selected. "
                        "All projects can use the flavor.")
    show_roles = False
    depends_on = ("error_id",)
    contributes = ("flavor_access",)

    def contribute(self, data, context):
        if data:
            member_field_name = self.get_member_field_name('member')
            context['flavor_access'] = data
        return context


class CreateError(workflows.Workflow):
    slug = "create_error"
    name = _("Create error")
    finalize_button_name = _("Create error")
    success_message = _('Created new error "%s".')
    failure_message = _('Unable to create error "%s".')
    success_url = "horizon:monitorint:errors:index"
    default_steps = (CreateErrorInfo,
                     UpdateFlavorAccess)

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


class UpdateErrorInfoAction(CreateErrorInfoAction):
    error_id = forms.CharField(widget=forms.widgets.HiddenInput)

    class Meta:
        name = _("Error Info")
        slug = 'update_info'
        help_text = _("From here you can edit the error details.")

    def clean(self):
        name = self.cleaned_data.get('name')
        id = self.cleaned_data.get('id')
        check = self.cleaned_data.get('check')
        
        return self.cleaned_data


class UpdateErrorInfo(workflows.Step):
    action_class = UpdateErrorInfoAction
    depends_on = ("error_id",)
    contributes = ("error_id",
                   "name",
                   "description",
                   "check",
                   "output_pattern",
                   "level",
                   "severity")

class UpdateError(workflows.Workflow):
    """base workflow
    """
    slug = "update_error"
    name = _("Edit error")
    finalize_button_name = _("Save")
    success_message = _('Modified error "%s".')
    failure_message = _('Unable to modify error "%s".')
    success_url = "horizon:monitoring:errors:index"
    default_steps = (UpdateErrorInfo,
                     UpdateFlavorAccess)

    def format_status_message(self, message):
        return message % self.context['name']

    def handle(self, request, data):
        flavor_projects = data["flavor_access"]
        is_public = not flavor_projects

        # Update flavor information
        try:
            flavor_id = data['flavor_id']
            # Grab any existing extra specs, because flavor edit is currently
            # implemented as a delete followed by a create.
            extras_dict = api.nova.flavor_get_extras(self.request,
                                                     flavor_id,
                                                     raw=True)
            # Mark the existing flavor as deleted.
            api.nova.flavor_delete(request, flavor_id)
            # Then create a new flavor with the same name but a new ID.
            # This is in the same try/except block as the delete call
            # because if the delete fails the API will error out because
            # active flavors can't have the same name.
            flavor = api.nova.flavor_create(request,
                                            data['name'],
                                            data['memory_mb'],
                                            data['vcpus'],
                                            data['disk_gb'],
                                            ephemeral=data['eph_gb'],
                                            swap=data['swap_mb'],
                                            is_public=is_public)
            if (extras_dict):
                api.nova.flavor_extra_set(request, flavor.id, extras_dict)
        except Exception:
            exceptions.handle(request, ignore=True)
            return False

        # Add flavor access if the flavor is not public.
        for project in flavor_projects:
            try:
                api.nova.add_tenant_to_flavor(request, flavor.id, project)
            except Exception:
                exceptions.handle(request, _('Modified flavor information, '
                                             'but unable to modify flavor '
                                             'access.'))
        return True
