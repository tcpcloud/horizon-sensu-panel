
from django.utils.translation import ugettext_lazy as _

from django.db import models
from horizon_contrib.api.models import APIModel
from horizon_contrib.common.model_registry import register

from .managers import ClientManager


class Client(APIModel):
    name = models.CharField('Name', primary_key=True)
    address = models.CharField(u"Address")
    subscriptions = models.CharField(u"Subscriptions")
    timestamp = models.CharField(u"Last Checkin")
    version = models.CharField(u"Sensu Version")

    objects = ClientManager()

    def __str__(self):
        return str(self.name)

    class Meta:
        abstract = True
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

register(Client)
