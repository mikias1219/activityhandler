from rest_framework import serializers

from .models import Budget, Expense, ExpenseCategory


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ["id", "name", "icon", "created_at"]
        read_only_fields = ["created_at"]


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            "id",
            "category",
            "amount",
            "currency",
            "expense_date",
            "note",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["id", "category", "month", "amount", "currency", "created_at"]
        read_only_fields = ["created_at"]
