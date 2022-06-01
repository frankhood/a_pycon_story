from django.apps import AppConfig


class PyconServiceConfigConfig(AppConfig):
    name = "pycon_service"

    def ready(self) -> None:
        super().ready()

        from . import receivers  # noqa
