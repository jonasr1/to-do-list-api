from rest_framework import serializers

from tasks.models import TaskHistory


class TaskHistorySerializer(serializers.ModelSerializer):

    class Meta:  # type: ignore
        model = TaskHistory
        fields = [
            "version",
            "task",
            "change_by",
            "change_date",
            "changes",
            "previous_states",
        ]
