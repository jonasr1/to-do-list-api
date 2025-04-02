from typing import Any, Dict
from rest_framework import serializers

from tasks.models import Task

class TaskSerializer(serializers.ModelSerializer):  
    user = serializers.SerializerMethodField(read_only=True) # Campo personalizado
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'is_completed','created_at', 'updated_at', 'user']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_user(self, obj: Task) -> Dict[str, Any]:
        return {
            'id': obj.user.id,
            'username': obj.user.username
        }

    def validate_title(self, title: str) -> str:
        '''Validates if the title already exists for the user.'''
        user = self.context['request'].user
        task_id = self.instance.id if self.instance else None
        if Task.objects.filter(user=user, title=title).exclude(id=task_id).exists():
            raise serializers.ValidationError('A task with this title already exists for this user.')
        return title
    