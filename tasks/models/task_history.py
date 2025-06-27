from typing import Any, ClassVar

from django.db import models

from users.models import User

from .task import Task


class TaskHistory(models.Model):
    objects: ClassVar[models.Manager["TaskHistory"]]
    version = models.PositiveIntegerField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="history")
    change_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    change_date = models.DateTimeField(auto_now=True)
    changes = models.JSONField()
    previous_states = models.JSONField()

    class Meta:
        unique_together = ["task", "version"]
        ordering = ["-version"]

    def __str__(self) -> str:
        return (
            f"Task History: {self.task.title} "  # type: ignore[attr-defined]
            f"(Version {self.version}) on {self.changes}"
        )

    @classmethod
    def create_from_task(
        cls,
        task: Task,
        change_by: User | None,
        changes: dict[str, Any],
        previous_states: dict[str, Any],
    ) -> "TaskHistory":
        version = task.latest_version + 1  # type: ignore
        history = cls(
            task=task,
            change_by=change_by,
            version=version,
            changes=changes,
            previous_states=previous_states,
        )
        task.latest_version = version  # type: ignore
        task.save(update_fields=["latest_version"])  # type: ignore[arg-type]
        history.save()
        return history
