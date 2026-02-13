from django.contrib import admin

from .models import Budget, Expense, ExpenseCategory


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "created_at"]
    search_fields = ["name"]
    raw_id_fields = ["user"]


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["amount", "currency", "category", "expense_date", "user", "created_at"]
    list_filter = ["currency", "expense_date"]
    search_fields = ["note"]
    raw_id_fields = ["user", "category"]
    date_hierarchy = "expense_date"


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ["month", "amount", "currency", "category", "user", "created_at"]
    list_filter = ["month"]
    raw_id_fields = ["user", "category"]
