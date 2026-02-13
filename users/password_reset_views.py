"""
Password reset flow: request (send email) and confirm (set new password).
"""
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User


class PasswordResetRequestView(APIView):
    """POST /api/v1/auth/password-reset/ — request password reset email."""

    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        email = request.data.get("email", "").strip().lower()
        if not email:
            return Response(
                {"detail": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.filter(email=email).first()
        if not user or not user.is_active:
            return Response(
                {"detail": "If an account exists with this email, you will receive a reset link."},
                status=status.HTTP_200_OK,
            )
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        base_url = getattr(settings, "FRONTEND_OR_BACKEND_URL", "http://localhost:8000").rstrip("/")
        reset_link = f"{base_url}/api/v1/auth/password-reset/confirm/?uid={uid}&token={token}"
        subject = "LifeOS — Password reset"
        body = (
            f"You requested a password reset for your LifeOS account ({user.email}).\n\n"
            f"Open this link to set a new password:\n{reset_link}\n\n"
            "If you didn't request this, ignore this email.\n\n— LifeOS"
        )
        try:
            user.email_user(subject, body, fail_silently=False)
        except Exception:
            return Response(
                {"detail": "Failed to send reset email. Try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        return Response(
            {"detail": "If an account exists with this email, you will receive a reset link."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    """POST /api/v1/auth/password-reset/confirm/ — set new password (uid & token in body or query)."""

    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        from django.utils.encoding import force_str
        from django.utils.http import urlsafe_base64_decode

        uid = request.data.get("uid") or request.query_params.get("uid")
        token = request.data.get("token") or request.query_params.get("token")
        new_password = request.data.get("new_password")
        new_password_confirm = request.data.get("new_password_confirm")

        if not all([uid, token, new_password]):
            return Response(
                {"detail": "uid, token, and new_password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if new_password != new_password_confirm:
            return Response(
                {"detail": "Passwords do not match."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(new_password) < 8:
            return Response(
                {"detail": "Password must be at least 8 characters."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"detail": "Invalid or expired reset link."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Invalid or expired reset link."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(new_password)
        user.save(update_fields=["password"])
        return Response(
            {"detail": "Password has been reset. You can now log in."},
            status=status.HTTP_200_OK,
        )
