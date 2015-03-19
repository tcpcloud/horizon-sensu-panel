
from django.db import models
from horizon_contrib.api.models import APIModel
from horizon_contrib.common.model_registry import register

from .managers import CheckManager


class Check(APIModel):
    name = models.CharField('name', primary_key=True)
    subscribers = models.CharField(u"Subscribers")
    handlers = models.CharField(u"Handlers")
    interval = models.CharField(u"Interval")
    command = models.CharField(u"Command")
    customer = models.CharField(u"Customer")
    occurrences = models.CharField(u"occurrences")
    asset = models.CharField(u"Asset")

    objects = CheckManager()

    def __repr__(self):
        return str(self.name)

    class Meta:
        abstract = True
        verbose_name = "check"
        verbose_name_plural = "checks"

register(Check)
