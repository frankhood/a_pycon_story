# -*- coding: utf-8 -*-
"""
a_pycon_story.management.commands.set_initial_site.

@created: 21/lug/2015
@last_important_modification: 21/lug/2015
"""
from __future__ import absolute_import, print_function, unicode_literals

import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

SITE_DOMAIN = getattr(settings, "SITE_DOMAIN", "http://localhost:8000/")
SITE_NAME = getattr(settings, "SITE_NAME", "My Website Name")


class Command(BaseCommand):
    def handle(self, *args, **options):
        current_site = Site.objects.get_current()
        current_site.domain = SITE_DOMAIN
        current_site.name = SITE_NAME
        current_site.save()
        print("The Site has been setted with domain '%s' and name '%s'" % (SITE_DOMAIN, SITE_NAME))
