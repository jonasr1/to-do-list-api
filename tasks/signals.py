from django.core.cache import cache
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from tasks.models import Task
from tasks.models_history import TaskHistory


@receiver([post_delete, post_save], sender=Task)
def clear_task_cache(sender, instance, **kwargs):
    if hasattr(instance, "_clearing_cache"):
        return
    instance._clearing_cache = True  # Checks if the cache has already been cleared
    user_id = instance.user.id
    print("Clearing task cache for user:", user_id)
    cache.delete(f"user_{user_id}_tasks")  # Remove task list cache
    cache.delete(f"user_stats_{user_id}")  # Remove statistics cache
    cache.delete(f"user_{user_id}_metrics")  # Remove metrics cache


@receiver(pre_save, sender=Task)
def create_task_history(sender, instance: Task, **kwargs):  # type: ignore
    if hasattr(
        instance, "_creating_history"
    ):  # Verifica se já estamos no meio de uma criação de TaskHistory
        return
    if (
        instance._state.adding
    ):  # Ignora se a instância está sendo criada (não atualizada)
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
            instance._creating_history = True  # type: ignore - atributo temporário
            TaskHistory.objects.create(
                task=instance,
                change_by=instance.user,
                changes=changes,
                previous_states={
                    "title": original.title,
                    "description": original.description,
                    "is_completed": original.is_completed,
                },
            )
        except Exception as e:
            print(f"Error saving history: {e}")
        finally:
            del instance._creating_history  # type: ignore
