import logging

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _  # noqa

logger = logging.getLogger(__name__)


class RemoteUserQuerySet(models.QuerySet):
    ...


class ResourceQuerySet(models.QuerySet):
    def for_user(self, remote_id: str):
        return self.filter(remote_users__remote_id__in=[remote_id])
