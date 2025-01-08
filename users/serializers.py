from typing import Any, Dict
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields: list[str] = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data: Dict[str, Any]) -> User:
        return User.objects.create_user(**validated_data)