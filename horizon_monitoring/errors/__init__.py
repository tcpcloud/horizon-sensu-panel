

from django.db import models
from horizon_contrib.api.models import APIModel
from horizon_contrib.common.model_registry import register

from .managers import Manager


class Error(APIModel):
    name = models.CharField(u"Check Name")
    check = models.CharField(u"check")
    output_pattern = models.CharField(u"output pattern")
    severity = models.CharField(u"severity")
    level = models.CharField(u"level")
    ownership = models.CharField(u"ownership")

    objects = Manager()

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = "known error"
        verbose_name_plural = "known errors"

register(Error)
