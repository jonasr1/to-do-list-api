from typing import Any

from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore[bad-override]
        model = User
        fields = ["id", "username", "password", "is_active"]
        extra_kwargs = {
            "password": {"write_only": True},
            "is_active": {"read_only": True},
            "is_staff": {"read_only": True},
            "is_superuser": {"read_only": True},
        }

    def create(self, validated_data: dict[str, Any]) -> User:
        password = validated_data.pop("password")
        return User.objects.create_user(**validated_data, password=password)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        if not attrs.get("username"):
            raise serializers.ValidationError({"username": ["This field is required."]})
        if not attrs.get("password"):
            raise serializers.ValidationError({"password": ["This field is required."]})
        return attrs
