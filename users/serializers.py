"""
User and auth serializers.
"""
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Current user profile."""

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "date_joined", "is_active"]
        read_only_fields = ["id", "email", "date_joined", "is_active"]


class RegisterSerializer(serializers.ModelSerializer):
    """Registration with password."""

    password = serializers.CharField(write_only=True, min_length=8, style={"input_type": "password"})
    password_confirm = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["email", "password", "password_confirm", "first_name", "last_name"]

    def validate(self, attrs: dict) -> dict:
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        attrs.pop("password_confirm")
        return attrs

    def create(self, validated_data: dict) -> User:
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user
