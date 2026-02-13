"""Productivity app tests."""

from datetime import date, timedelta

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User

from .models import Task


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="u@example.com", password="pass123", first_name="U", last_name="U"
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.mark.django_db
class TestTaskCRUD:
    def test_list_tasks_empty(self, auth_client):
        resp = auth_client.get("/api/v1/tasks/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["results"] == []

    def test_create_task(self, auth_client, user):
        resp = auth_client.post(
            "/api/v1/tasks/",
            {
                "title": "My task",
                "notes": "Note",
                "due_date": "2025-03-01",
                "priority": "urgent_important",
                "status": "todo",
            },
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.data["title"] == "My task"
        assert Task.objects.filter(user=user).count() == 1

    def test_today_view(self, auth_client, user):
        Task.objects.create(
            user=user, title="Today task", due_date=date.today(), status=Task.Status.TODO
        )
        Task.objects.create(
            user=user,
            title="Later",
            due_date=date.today() + timedelta(days=7),
            status=Task.Status.TODO,
        )
        resp = auth_client.get("/api/v1/tasks/today/")
        assert resp.status_code == status.HTTP_200_OK
        results = resp.data if isinstance(resp.data, list) else resp.data.get("results", resp.data)
        assert len(results) == 1
        assert results[0]["title"] == "Today task"

    def test_task_detail_update_delete(self, auth_client, user):
        task = Task.objects.create(user=user, title="Original", status=Task.Status.TODO)
        resp = auth_client.get(f"/api/v1/tasks/{task.pk}/")
        assert resp.status_code == status.HTTP_200_OK
        resp = auth_client.patch(f"/api/v1/tasks/{task.pk}/", {"status": "done"}, format="json")
        assert resp.status_code == status.HTTP_200_OK
        task.refresh_from_db()
        assert task.status == Task.Status.DONE
        resp = auth_client.delete(f"/api/v1/tasks/{task.pk}/")
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert not Task.objects.filter(pk=task.pk).exists()
