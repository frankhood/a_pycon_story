# -*- coding: utf-8 -*-
"""
a_pycon_story.management.commands.set_initial_site.

@created: 21/lug/2015
@last_important_modification: 21/lug/2015
"""
from __future__ import absolute_import, print_function, unicode_literals

import logging

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext, gettext_lazy as _  # noqa

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info("Starting scheduling of processes...")
        logger.info("...Scheduling of processes ended")
