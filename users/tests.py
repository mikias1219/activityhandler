"""Users app tests."""
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="test@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User",
    )


@pytest.mark.django_db
class TestRegister:
    def test_register_success(self, api_client):
        resp = api_client.post(
            "/api/v1/auth/register/",
            {"email": "new@example.com", "password": "securepass123", "password_confirm": "securepass123", "first_name": "New", "last_name": "User"},
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED
        assert "user" in resp.data
        assert resp.data["user"]["email"] == "new@example.com"
        assert User.objects.filter(email="new@example.com").exists()

    def test_register_password_mismatch(self, api_client):
        resp = api_client.post(
            "/api/v1/auth/register/",
            {"email": "new@example.com", "password": "pass123", "password_confirm": "pass456", "first_name": "A", "last_name": "B"},
            format="json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogin:
    def test_login_success(self, api_client, user):
        resp = api_client.post(
            "/api/v1/auth/login/",
            {"email": "test@example.com", "password": "testpass123"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK
        assert "access" in resp.data
        assert "refresh" in resp.data

    def test_login_invalid_credentials(self, api_client, user):
        resp = api_client.post(
            "/api/v1/auth/login/",
            {"email": "test@example.com", "password": "wrong"},
            format="json",
        )
        assert resp.status_code in (status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED)


@pytest.mark.django_db
class TestMe:
    def test_me_authenticated(self, api_client, user):
        api_client.force_authenticate(user=user)
        resp = api_client.get("/api/v1/me/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["email"] == user.email

    def test_me_unauthenticated(self, api_client):
        resp = api_client.get("/api/v1/me/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPasswordReset:
    def test_password_reset_request_returns_200_even_unknown_email(self, api_client):
        resp = api_client.post("/api/v1/auth/password-reset/", {"email": "nonexistent@example.com"}, format="json")
        assert resp.status_code == status.HTTP_200_OK

    def test_password_reset_request_valid_email(self, api_client, user):
        resp = api_client.post("/api/v1/auth/password-reset/", {"email": "test@example.com"}, format="json")
        assert resp.status_code == status.HTTP_200_OK

    def test_password_reset_confirm_success(self, api_client, user):
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode
        from django.contrib.auth.tokens import default_token_generator

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        resp = api_client.post(
            "/api/v1/auth/password-reset/confirm/",
            {"uid": uid, "token": token, "new_password": "newpass123", "new_password_confirm": "newpass123"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.check_password("newpass123")

    def test_password_reset_confirm_invalid_token(self, api_client, user):
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        resp = api_client.post(
            "/api/v1/auth/password-reset/confirm/",
            {"uid": uid, "token": "invalid", "new_password": "newpass123", "new_password_confirm": "newpass123"},
            format="json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
