# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext, gettext_lazy as _  # noqa

logger = logging.getLogger(__name__)


class User(AbstractUser):
    class Meta:
        """User Meta."""

        verbose_name = _("User")
        verbose_name_plural = _("Users")
