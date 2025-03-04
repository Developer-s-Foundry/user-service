from django.db.models import Model


class DatabaseRouter:
    """
    Router to route models to their respective databases
    """

    def db_for_read(self, model: Model, **hints: dict) -> str:
        if model._meta.app_label == "mongo":
            return "mongo"
        elif model._meta.app_label == "postgres":
            return "pg"
        return None

    def db_for_write(self, model: Model, **hints: dict) -> str:
        if model._meta.app_label == "mongo":
            return "mongo"
        elif model._meta.app_label == "postgres":
            return "pg"
        return None

    def allow_relation(self, obj1: Model, obj2: Model, **hints: dict) -> bool:
        # Allow relations if both models are in the same database
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        return None

    def allow_migrate(
        self, db: str, app_label: str, model_name: str | None = None, **hints: dict
    ) -> bool:
        if app_label == "mongo":
            return db == "mongo"
        elif app_label == "postgres":
            return db == "pg"
        return None
