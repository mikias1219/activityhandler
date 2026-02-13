"""
Habits: definitions and check-ins with streak calculation.
"""
from django.conf import settings
from django.db import models


class Habit(models.Model):
    class TargetFrequency(models.TextChoices):
        DAILY = "daily", "Daily"
        WEEKLY = "weekly", "Weekly"
        CUSTOM = "custom", "Custom"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
    )
    name = models.CharField(max_length=255)
    target_frequency = models.CharField(
        max_length=20,
        choices=TargetFrequency.choices,
        default=TargetFrequency.DAILY,
    )
    target_count = models.PositiveSmallIntegerField(
        default=1,
        help_text="e.g. 1 per day, 3 per week",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class HabitCheckIn(models.Model):
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name="check_ins",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habit_check_ins",
    )
    check_date = models.DateField(db_index=True)
    completed = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-check_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["habit", "check_date"],
                name="unique_habit_check_per_day",
            ),
        ]
        indexes = [
            models.Index(fields=["habit", "check_date"]),
        ]

    def __str__(self) -> str:
        return f"{self.habit.name} @ {self.check_date}"
