from django.db.models import Count, Q

from tasks.domain import TaskStats
from tasks.models import Task
from users.models import User


def calculate_task_stats(user: User) -> TaskStats:
    stats = Task.objects.filter(user=user).aggregate(
        total=Count("id"),
        completed=Count("id", filter=Q(is_completed=True)),
    )
    total = stats["total"]
    completed = stats["completed"]
    pending = total - completed
    percentage = (completed / total * 100) if total > 0 else 0.0
    return TaskStats(
        total_tasks=total,
        completed_tasks=completed,
        pending_tasks=pending,
        completion_percentage=percentage,
    )
