

from django.db import models
from horizon_contrib.api.models import DictModel
from horizon_contrib.common.model_registry import register

from .managers import CheckManager


class Check(DictModel):
    name = models.CharField('name')
    subscribers = models.CharField(u"Subscribers")
    handlers = models.CharField(u"Handlers")
    interval = models.CharField(u"Interval")
    command = models.CharField(u"Command")
    customer = models.CharField(u"Customer")
    occurrences = models.CharField(u"occurrences")
    asset = models.CharField(u"Asset")
    #workarounds = models.CharField(u"Asset")

    objects = CheckManager()

    def __unicode__(self):
        return self["name"]

    class Meta:
        abstract = True
        verbose_name = "check"
        verbose_name_plural = "checks"

register(Check)
