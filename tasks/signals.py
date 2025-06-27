import logging
import weakref
from typing import TYPE_CHECKING, Any

from django.core.cache import cache
from django.db.models.base import Model
from django.db.models.signals import post_delete, post_save, pre_save
from django.db.utils import DatabaseError
from django.dispatch import receiver

from .models import Task, TaskHistory

if TYPE_CHECKING:
    from users.models import User

logger = logging.getLogger(__name__)

# Armazena referências fracas a instâncias que já passaram pelo cache ou histórico
_cleared_cache = weakref.WeakSet()
_created_history = weakref.WeakSet()

@receiver([post_delete, post_save], sender=Task)
def clear_task_cache(sender: type[Model], instance: Task, **_kwargs: dict[str, Any]) -> None:  # noqa: E501 # pylint: disable=unused-argument
    if instance in _cleared_cache:
        return
    _cleared_cache.add(instance)  # Mark this instance as cleared
    user_id = instance.user.id
    logger.info("Clearing task cache for user: %s", user_id)
    cache.delete(f"user_{user_id}_tasks")  # Remove task list cache
    cache.delete(f"user_stats_{user_id}")  # Remove statistics cache
    cache.delete(f"user_{user_id}_metrics")  # Remove metrics cache


@receiver(pre_save, sender=Task)
def create_task_history(sender: type[Model], instance: Task, **_kwargs: dict[str, Any]) -> None:  # noqa: E501 # pylint: disable=unused-argument
    if instance in _created_history or instance._state.adding:  # Verifica se já estamos no meio de uma criação de TaskHistory  # noqa: E501, SLF001
        return
    try:
        original = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        return
    original = Task.objects.get(pk=instance.pk)
    changes = {}
    for field in ["title", "description", "is_completed"]:
        original_value = getattr(original, field)
        new_value = getattr(instance, field)
        if original_value != new_value:
            changes[field] = {"old": original_value, "new": new_value}
    if changes:
        try:
            _created_history.add(instance)
            user: User = instance.user
            TaskHistory.create_from_task(
                task=instance,
                change_by=user,
                changes=changes,
                previous_states={
                    "title": original.title,
                    "description": original.description,
                    "is_completed": original.is_completed,
                },
            )
        except DatabaseError:
            logger.exception("Error saving task history: %s")
