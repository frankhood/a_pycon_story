"""
a_pycon_story.management.commands.startapp_fh.

@created: 14/feb/2022
"""
from __future__ import absolute_import, print_function, unicode_literals

import logging

from cookiecutter.main import cookiecutter
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    How to use.

    ./manage.py startapp_fh
    """

    FH_STARTAPP_URL = "https://gitlab.com/fh-start/fh-startapp-cookiecutter-template.git"

    def handle(self, **options):
        cookiecutter(
            self.FH_STARTAPP_URL,
            extra_context={
                "project_slug": "a_pycon_story",
            },
        )
