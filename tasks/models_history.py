from django.db import models
from tasks.models import Task
from users.models import User

class TaskHistory(models.Model):
    version = models.PositiveIntegerField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='history')
    change_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    change_date = models.DateTimeField(auto_now=True)
    changes = models.JSONField()
    previous_states = models.JSONField()

    def __str__(self):
        return f'Task History: {self.task.title} (Version {self.version}) on {self.changes}'
    
    def save(self, *args, **kwargs): # type: ignore
        if not self.version:
            self.version = self.task.latest_version + 1
            self.task.latest_version = self.version
            self.task.save(update_fields=['latest_version'])
        super().save(*args, **kwargs)   
    
    class Meta:
        unique_together = ['task', 'version']
        ordering = ['-version']
