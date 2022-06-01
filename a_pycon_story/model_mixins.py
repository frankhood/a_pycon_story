# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _  # noqa
from django_extensions.db.models import TimeStampedModel
from self_aware_model.models import SelfAwareModelMixin
from slug_model_mixin.model_mixins import SlugModelMixin

logger = logging.getLogger(__name__)


class BaseModel(SelfAwareModelMixin, TimeStampedModel):
    class Meta:
        abstract = True
        ordering = ["-created"]
        get_latest_by = "-created"

    @property
    def obj_meta(self):
        return self.__class__._meta

    @property
    def admin_absolute_url(self):
        logger.warning("admin_absolute_url is deprecated.. Use admin_change_url instead")
        return self.admin_change_url

    @property
    def admin_change_url(self):
        from django.urls import reverse

        url_context = {"app_label": self._meta.app_label, "model_name": self._meta.model_name}
        return reverse("admin:{app_label}_{model_name}_change".format(**url_context), args=(self.id,))

    @classmethod
    def admin_changelist_url(cls):
        from django.urls import reverse

        url_context = {"app_label": cls._meta.app_label, "model_name": cls._meta.model_name}
        return reverse("admin:{app_label}_{model_name}_changelist".format(**url_context))

    @classmethod
    def admin_add_url(cls):
        from django.urls import reverse

        url_context = {"app_label": cls._meta.app_label, "model_name": cls._meta.model_name}
        return reverse("admin:{app_label}_{model_name}_add".format(**url_context))

    def app_label(self):
        # Serve per ritrovarsi a template l'app_label
        return self._meta.app_label

    def model_name(self):
        # Serve per ritrovarsi a template il model_name
        return self._meta.model_name


class BaseCategory(SlugModelMixin, BaseModel):
    slugged_field = "name"
    slug_unique = True
    force_slugify = True

    name = models.CharField(_("name"), max_length=155)

    class Meta(BaseModel.Meta):
        abstract = True

    def __str__(self):
        return self.name
