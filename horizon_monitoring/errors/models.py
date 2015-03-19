
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


class Error(APIModel):
    id = models.CharField(u"ID", primary_key=True)
    name = models.CharField(u"Check Name")
    check = models.CharField(u"check")
    output_pattern = models.CharField(u"output pattern")

    level = models.CharField(max_length=55, verbose_name=_(
        'level'), default='level1', choices=LEVEL_CHOICES)
    severity = models.CharField(max_length=55, verbose_name=_(
        'severity'), default='medium', choices=SEVERITY_CHOICES)
    ownership = models.CharField(max_length=55, verbose_name=_(
        'ownership'), default='cloudlab', choices=OWNERSHIP_CHOICES)

    objects = Manager()

    def __repr__(self):
        return str(self.name)

    class Meta:
        abstract = True
        verbose_name = "known error"
        verbose_name_plural = "known errors"

register(Error)
