from rest_framework import serializers
from tasks.models_history import TaskHistory

class TaskHistorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TaskHistory
        fields = ['version', 'task', 'change_by', 'change_date', 'changes', 'previous_states']
