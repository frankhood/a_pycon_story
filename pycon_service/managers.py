import logging

from django.db import models
from django.utils.translation import ugettext, gettext_lazy as _  # noqa

logger = logging.getLogger(__name__)


class RemoteUserManager(models.Manager):
    ...


class ResourcerManager(models.Manager):
    ...
