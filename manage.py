#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import configurations
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())  # does not override already set variables
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "a_pycon_story.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Local")


def main():
    """Run administrative tasks."""
    load_dotenv(find_dotenv())  # does not override already set variables
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "a_pycon_story.settings")
    try:
        from configurations.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
else:
    # For django-q and testing from Pycharm pourpose only
    configurations.setup()
