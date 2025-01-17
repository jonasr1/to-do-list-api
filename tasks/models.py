import uuid
from django.db import models
from django.core.exceptions import ValidationError
from core.models import TimeStampedModel
from users.models import User

class Task(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    
    def clean(self) -> None:
        super().clean()
        if not self.title.strip():
            raise ValidationError({'title': ['The title cannot be empty or contain only spaces']})
        if not (self.description or '').strip():
            self.description = ''
    
    def save(self, *args, **kwargs): # type: ignore
        self.clean()
        super().save(*args, **kwargs)
    
    class Meta: # type: ignore
        constraints = [
            models.UniqueConstraint(fields=['title', 'user'], name='unique_title_per_user')
        ]
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
