"""AI Coach tests."""

import pytest
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="u@example.com", password="pass123", first_name="U", last_name="U"
    )


@pytest.fixture
def auth_client(user):
    c = APIClient()
    c.force_authenticate(user=user)
    return c


@pytest.mark.django_db
def test_what_to_do_now_returns_suggestions(auth_client, user):
    resp = auth_client.get("/api/v1/ai/what-to-do-now/")
    assert resp.status_code == 200
    assert "suggestions" in resp.data
    assert "message" in resp.data
