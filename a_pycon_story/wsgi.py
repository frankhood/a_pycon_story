"""
WSGI config for A Pycon Story project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/
"""

import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())  # does not override already set variables
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "a_pycon_story.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Local")

from configurations.wsgi import get_wsgi_application  # noqa isort:skip

application = get_wsgi_application()
