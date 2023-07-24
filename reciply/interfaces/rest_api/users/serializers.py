# Standard library imports
from typing import Any

# Third party imports
from rest_framework import serializers

# Django imports
from django.contrib.auth import models as auth_models


class RegisterUser(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    email = serializers.EmailField()
    password1 = serializers.CharField(min_length=6)
    password2 = serializers.CharField(min_length=6)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def validate_username(self, username: str) -> str:
        if auth_models.User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already taken")
        return username
