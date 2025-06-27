from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"  # type: ignore
    name = "tasks"

    def ready(self) -> None:
        from . import signals  # pylint: disable=all
