
from django.utils.translation import ugettext_lazy as _
import horizon
from horizon_monitoring.dashboard import MonitoringDashboard, include_gitlab
from django.conf import settings

class ProjectsPanel(horizon.Panel):
    name = _("Gitlab projects")
    slug = 'projects'

MonitoringDashboard.register(ProjectsPanel)
