import importlib

from django.core.signals import setting_changed
from django.dispatch import receiver

from . import settings as app_settings


@receiver(setting_changed)
def app_settings_reload_handler(**kwargs):
    if kwargs["setting"] in ["USER_CLIENT_CLASS", "USER_SERVICE_API_KEY", "USER_SERVICE_BASE_URL"]:
        importlib.reload(app_settings)
