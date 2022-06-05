# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.apps.config import AppConfig
from django.utils.translation import ugettext, gettext_lazy as _  # noqa


class ProfilesConfig(AppConfig):
    name = "profiles"
    verbose_name = _("Profiles")

    def ready(self):
        """Load receivers here."""
