from calendar import monthrange
from datetime import date

from django.db.models import Sum
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Budget, Expense, ExpenseCategory
from .serializers import BudgetSerializer, ExpenseCategorySerializer, ExpenseSerializer


class ExpenseCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExpenseCategory.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExpenseCategory.objects.filter(user=self.request.user)


class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Expense.objects.filter(user=self.request.user).select_related("category")
        month = self.request.query_params.get("month")  # YYYY-MM
        category_id = self.request.query_params.get("category_id")
        if month:
            try:
                y, m = map(int, month.split("-"))
                start = date(y, m, 1)
                _, last = monthrange(y, m)
                end = date(y, m, last)
                qs = qs.filter(expense_date__range=[start, end])
            except (ValueError, IndexError):
                pass
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).select_related("category")


class ExpenseReportView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        """Report: sum by category for a given month. ?month=YYYY-MM"""
        month = request.query_params.get("month")
        if not month:
            # Default: current month
            today = timezone.now().date()
            month = today.strftime("%Y-%m")
        try:
            y, m = map(int, month.split("-"))
            start = date(y, m, 1)
            _, last = monthrange(y, m)
            end = date(y, m, last)
        except (ValueError, IndexError):
            return Response(
                {"detail": "Invalid month. Use YYYY-MM."},
                status=400,
            )
        qs = (
            Expense.objects.filter(
                user=request.user,
                expense_date__range=[start, end],
            )
            .values("category__name", "category_id")
            .annotate(total=Sum("amount"))
        )
        total = sum(r["total"] for r in qs)
        return Response(
            {
                "month": month,
                "by_category": list(qs),
                "total": total,
            }
        )


class BudgetListCreateView(generics.ListCreateAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user).select_related("category")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BudgetDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
