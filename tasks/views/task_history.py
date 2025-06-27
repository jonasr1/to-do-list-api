
import uuid

from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from tasks.models import TaskHistory
from tasks.serializers import TaskHistorySerializer


class TaskHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet to manage task history.
    Supports:
    - List all task history entries (GET /task-history)
    - List history entries for a specific task(GET /task-history?task=<task_id>)
    """

    queryset = TaskHistory.objects.all()
    serializer_class = TaskHistorySerializer  # type: ignore[bad-override]
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:  # type: ignore
        """
        Returns the TaskHistory queryset for the authenticated user.

        If the "task" query parameter is provided and is a valid UUID,
        returns the history only for that specific task belonging to the user.

        If the "task" parameter is missing, returns the entire task history
        for the authenticated user.

        Raises ValidationError with HTTP 400 if the provided UUID is invalid.
        """
        task_id = self.request.GET.get("task", None)
        if task_id:
            try:
                task_uuid = uuid.UUID(task_id.strip().strip('"“”'))
            except (ValueError, TypeError) as exc:
                msg = "Invalid UUID format in 'task' parameter."
                raise ValidationError(msg) from exc
            return TaskHistory.objects.filter(
                task_id=task_uuid, task__user=self.request.user
            )
        return TaskHistory.objects.filter(task__user=self.request.user)
