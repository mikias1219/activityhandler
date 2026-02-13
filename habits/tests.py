"""Habits app tests."""

from datetime import date, timedelta

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User

from .models import Habit, HabitCheckIn
from .services import get_streak


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
class TestHabitCRUD:
    def test_list_create_habit(self, auth_client, user):
        resp = auth_client.get("/api/v1/habits/")
        assert resp.status_code == status.HTTP_200_OK
        resp = auth_client.post(
            "/api/v1/habits/",
            {"name": "Morning run", "target_frequency": "daily", "target_count": 1},
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.data["name"] == "Morning run"
        assert Habit.objects.filter(user=user).count() == 1

    def test_check_in_and_streak(self, auth_client, user):
        habit = Habit.objects.create(user=user, name="Read", target_frequency="daily")
        resp = auth_client.post(
            f"/api/v1/habits/{habit.pk}/check-ins/",
            {"check_date": date.today().isoformat(), "completed": True},
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED
        resp = auth_client.get(f"/api/v1/habits/{habit.pk}/streak/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["current_streak"] == 1


@pytest.mark.django_db
def test_get_streak_consecutive_days(user):
    habit = Habit.objects.create(user=user, name="Run", target_frequency="daily")
    today = date.today()
    for i in range(3):
        HabitCheckIn.objects.create(
            habit=habit, user=user, check_date=today - timedelta(days=i), completed=True
        )
    assert get_streak(habit) == 3
