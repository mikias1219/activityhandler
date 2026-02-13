"""Core app tests."""
import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_health_endpoint():
    client = Client()
    response = client.get("/api/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "lifeos"
