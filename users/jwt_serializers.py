"""JWT token serializers — email-based login."""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Accept email + password for login (no username)."""

    username_field = "email"

    def validate(self, attrs):
        email = (attrs.get("email") or "").strip().lower()
        password = attrs.get("password")
        if not email or not password:
            raise serializers.ValidationError("email and password are required.")
        user = User.objects.filter(email=email).first()
        if not user or not user.check_password(password) or not user.is_active:
            raise serializers.ValidationError("Invalid email or password.")
        refresh = RefreshToken.for_user(user)
        refresh["email"] = user.email
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {"id": user.id, "email": user.email},
        }
