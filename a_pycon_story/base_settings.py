import os

from configurations import values


class BaseSettings(object):
    """We use this class to have these configurations available for all settings."""

    SECRET_KEY = values.SecretValue()

    DEBUG = values.BooleanValue(True)

    ALLOWED_HOSTS = values.ListValue([])

    # Local time zone for this installation. Choices can be found here:
    # http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
    # although not all choices may be available on all operating systems.
    # In a Windows environment this must be set to your system time zone.
    TIME_ZONE = "Europe/Rome"

    # Language code for this installation. All choices can be found here:
    # http://www.i18nguy.com/unicode/language-identifiers.html
    LANGUAGE_CODE = "it"

    SITE_ID = 1

    FORMAT_MODULE_PATH = [
        "formats",
    ]

    # If setted See debug comments, when DEBUG is True and Receive X headers in admindocs if the XViewMiddleware is installed (see The Django admin documentation generator)
    INTERNAL_IPS = (("127.0.0.1",),)

    PROJECT_PATH, _ = os.path.split(os.path.split(os.path.realpath(__file__))[0])

    # List of finder classes that know how to find static files in
    # various locations.
    STATICFILES_FINDERS = (
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    )

    TEST_RUNNER = "django.test.runner.DiscoverRunner"
    TEMPLATE_DEBUG = DEBUG
    ACTIVE_DEBUG_TOOLBAR = False

    # profile settings
    AUTH_USER_MODEL = "profiles.User"
