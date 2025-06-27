from typing import Any

from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)  # Campo personalizado

    class Meta:  # type: ignore[bad-override]
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "is_completed",
            "created_at",
            "updated_at",
            "user",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def get_user(self, obj: Task) -> dict[str, Any]:
        user = obj.user
        return {"id": user.id, "username": user.username}

    def validate_title(self, title: str) -> str:
        """Validates if the title already exists for the user."""
        user = self.context["request"].user
        task_id = task_id = getattr(self.instance, "id", None)
        if Task.objects.filter(user=user, title=title).exclude(id=task_id).exists():
            msg = "A task with this title already exists for this user."
            raise serializers.ValidationError({"title": [msg]})  # pyrefly: ignore [bad-argument-type]  # noqa: E501
        return title
