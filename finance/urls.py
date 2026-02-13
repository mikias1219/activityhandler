from django.urls import path

from .views import (
    BudgetDetailView,
    BudgetListCreateView,
    ExpenseCategoryDetailView,
    ExpenseCategoryListCreateView,
    ExpenseDetailView,
    ExpenseListCreateView,
    ExpenseReportView,
)

urlpatterns = [
    path(
        "expense-categories/", ExpenseCategoryListCreateView.as_view(), name="expense-category-list"
    ),
    path(
        "expense-categories/<int:pk>/",
        ExpenseCategoryDetailView.as_view(),
        name="expense-category-detail",
    ),
    path("expenses/", ExpenseListCreateView.as_view(), name="expense-list"),
    path("expenses/report/", ExpenseReportView.as_view(), name="expense-report"),
    path("expenses/<int:pk>/", ExpenseDetailView.as_view(), name="expense-detail"),
    path("budgets/", BudgetListCreateView.as_view(), name="budget-list"),
    path("budgets/<int:pk>/", BudgetDetailView.as_view(), name="budget-detail"),
]
