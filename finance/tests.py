"""Finance app tests."""

from datetime import date

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User

from .models import Budget, Expense, ExpenseCategory


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


@pytest.fixture
def category(user):
    return ExpenseCategory.objects.create(user=user, name="Food")


@pytest.mark.django_db
class TestExpenseCategoryAndExpenses:
    def test_create_category_and_expense(self, auth_client, user):
        resp = auth_client.post(
            "/api/v1/expense-categories/", {"name": "Transport", "icon": "car"}, format="json"
        )
        assert resp.status_code == status.HTTP_201_CREATED
        cat_id = resp.data["id"]
        resp = auth_client.post(
            "/api/v1/expenses/",
            {
                "category": cat_id,
                "amount": "50.00",
                "currency": "USD",
                "expense_date": "2025-02-01",
                "note": "Bus",
            },
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.data["amount"] == "50.00"

    def test_expense_report(self, auth_client, user, category):
        Expense.objects.create(
            user=user, category=category, amount=100, expense_date=date(2025, 2, 15), currency="USD"
        )
        resp = auth_client.get("/api/v1/expenses/report/?month=2025-02")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["month"] == "2025-02"
        assert float(resp.data["total"]) == 100


@pytest.mark.django_db
class TestBudget:
    def test_create_budget(self, auth_client, user, category):
        resp = auth_client.post(
            "/api/v1/budgets/",
            {"category": category.pk, "month": "2025-02-01", "amount": "500", "currency": "USD"},
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED
        assert Budget.objects.filter(user=user).count() == 1
