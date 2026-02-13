"""
Productivity: tasks (GTD-style) with Eisenhower priority.
"""

from django.conf import settings
from django.db import models


class Task(models.Model):
    """Single task with priority and status."""

    class Priority(models.TextChoices):
        URGENT_IMPORTANT = "urgent_important", "Urgent & Important"
        URGENT_NOT_IMPORTANT = "urgent_not_important", "Urgent, Not Important"
        NOT_URGENT_IMPORTANT = "not_urgent_important", "Not Urgent, Important"
        NOT_URGENT_NOT_IMPORTANT = "not_urgent_not_important", "Not Urgent, Not Important"

    class Status(models.TextChoices):
        TODO = "todo", "To Do"
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True, db_index=True)
    priority = models.CharField(
        max_length=32,
        choices=Priority.choices,
        default=Priority.NOT_URGENT_IMPORTANT,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["due_date", "created_at"]
        indexes = [
            models.Index(fields=["user", "due_date", "status"]),
        ]

    def __str__(self) -> str:
        return self.title
