# -*- coding: UTF-8 -*-
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _
from horizon import tables
from horizon_contrib.tables.actions import FilterAction
"""
  {
    "id": 4,
    "description": null,
    "default_branch": "master",
    "public": false,
    "visibility_level": 0,
    "ssh_url_to_repo": "git@example.com:diaspora/diaspora-client.git",
    "http_url_to_repo": "http://example.com/diaspora/diaspora-client.git",
    "web_url": "http://example.com/diaspora/diaspora-client",
    "owner": {
      "id": 3,
      "name": "Diaspora",
      "created_at": "2013-09-30T13: 46: 02Z"
    },
    "name": "Diaspora Client",
    "name_with_namespace": "Diaspora / Diaspora Client",
    "path": "diaspora-client",
    "path_with_namespace": "diaspora/diaspora-client",
    "issues_enabled": true,
    "merge_requests_enabled": true,
    "wall_enabled": false,
    "wiki_enabled": true,
    "snippets_enabled": false,
    "created_at": "2013-09-30T13: 46: 02Z",
    "last_activity_at": "2013-09-30T13: 46: 02Z",
    "namespace": {
      "created_at": "2013-09-30T13: 46: 02Z",
      "description": "",
      "id": 3,
      "name": "Diaspora",
      "owner_id": 1,
      "path": "diaspora",
      "updated_at": "2013-09-30T13: 46: 02Z"
    },
    "archived": false
  },
"""

class ProjectsTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_("Name"), link=(lambda v: v.get("web_url")))
    description = tables.Column('description', verbose_name=_("Description"))
    http_url_to_repo = tables.Column('http_url_to_repo', verbose_name=_("Key"))
    default_branch = tables.Column('default_branch', verbose_name=_("Default Branch"))

    def get_object_id(self, datum):
        return datum['id']

    def get_object_display(self, datum):
        return datum['name']

    class Meta:
        name = "keys"
        verbose_name = _("Deploy Keys")
        table_actions= (FilterAction, )
