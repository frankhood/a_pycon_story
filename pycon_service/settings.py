from django.conf import settings

USER_CLIENT_CLASS = getattr(settings, "USER_CLIENT_CLASS", "pycon_service.clients.UserClient")
USER_SERVICE_API_KEY = getattr(settings, "USER_SERVICE_API_KEY", None)
USER_SERVICE_BASE_URL = getattr(settings, "USER_SERVICE_BASE_URL", None)
