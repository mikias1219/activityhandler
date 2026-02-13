from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Task.objects.filter(user=self.request.user)
        due_date = self.request.query_params.get("due_date")
        status = self.request.query_params.get("status")
        priority = self.request.query_params.get("priority")
        if due_date:
            qs = qs.filter(due_date=due_date)
        if status:
            qs = qs.filter(status=status)
        if priority:
            qs = qs.filter(priority=priority)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskTodayView(generics.ListAPIView):
    """Today's tasks (daily planner)."""
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        today = timezone.now().date()
        return Task.objects.filter(
            user=self.request.user,
            due_date=today,
            status__in=[Task.Status.TODO, Task.Status.IN_PROGRESS],
        ).order_by("priority", "created_at")
