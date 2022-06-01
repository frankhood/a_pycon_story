# -*- coding: utf-8 -*-
"""
a_pycon_story.management.commands.setup_website.

@created: 21/lug/2015
@last_important_modification: 21/lug/2015
"""
from __future__ import absolute_import, print_function, unicode_literals

import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext, ugettext_lazy as _  # noqa

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command("set_initial_site")
        # Insert here other initial Fixtures..
        # call_command('loaddata', 'project/apps/../initial_polls.json')
        print("Setup Completed")
