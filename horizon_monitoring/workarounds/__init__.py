from django.db import models
from django.utils.translation import ugettext_lazy as _
from horizon_contrib.api.models import APIModel
from horizon_contrib.common.model_registry import register

from .managers import Manager

LEVEL_CHOICES = (
    ("l1", u"Level 1"),
    ("l2", u"Level 2"),
)

SEVERITY_CHOICES = (
    ("int", u"Internal"),
    ("999", u"SLA 99.9"),
    ("9999", u"SLA 99.99"),
)

OWNERSHIP_CHOICES = (
    ("cloud", u"Cloud"),
    ("network", u"Network"),
    ("hardware", u"Hardware"),
)

ENGINE_CHOICES = (
    ("salt", u"Salt call"),
    ("jenkins", u"Jenkins job"),
    ("misc", u"Misc"),
)


class Workaround(APIModel):
    id = models.CharField(verbose_name=_('known error'), primary_key=True)
    known_error = models.CharField(verbose_name=_('known error'))
    description = models.TextField(verbose_name=_('description'), blank=True)
    temporary = models.BooleanField(
        max_length=255, verbose_name=_('temporary'))
    engine = models.CharField(max_length=255, verbose_name=_(
        'engine'), default='salt', choices=ENGINE_CHOICES)
    action = models.TextField(verbose_name=_('description'), blank=True)

    objects = Manager()

    @property
    def error_detail(self):
        return self.known_error

    class Meta:
        abstract = True
        verbose_name = _("workaround")
        verbose_name_plural = _("workarounds")

register(Workaround)
