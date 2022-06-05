import uuid

from django.db import models
from django.utils.translation import ugettext, gettext_lazy as _  # noqa

from a_pycon_story.model_mixins import BaseModel
from pycon_service import managers as app_managers, querysets as app_querysets


class RemoteUser(BaseModel):

    objects = app_managers.RemoteUserManager.from_queryset(app_querysets.RemoteUserQuerySet)()

    remote_id = models.UUIDField(_("Remote ID"), unique=True, primary_key=True, default=uuid.uuid4)

    class Meta(BaseModel.Meta):
        """RemoteUser Meta."""

        verbose_name = _("RemoteUser")
        verbose_name_plural = _("RemoteUsers")

    def __str__(self):
        return str(self.remote_id)


class Resource(BaseModel):

    objects = app_managers.ResourcerManager.from_queryset(app_querysets.ResourceQuerySet)()

    remote_users = models.ManyToManyField(RemoteUser, verbose_name=_("Remote users"), related_name="resources")
    name = models.CharField(_("Name"), max_length=255, blank=True, default="")
    file = models.FileField(_("File"), upload_to="resources/")

    class Meta(BaseModel.Meta):
        """RemoteUser Meta."""

        verbose_name = _("RemoteUser")
        verbose_name_plural = _("RemoteUsers")

    def __str__(self):
        return self.name
