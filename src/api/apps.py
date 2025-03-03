from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.api"

    def ready(self) -> None:
        from src.utils.svcs.registry import init_registry, close_registry

        init_registry(self)
        close_registry(self)
