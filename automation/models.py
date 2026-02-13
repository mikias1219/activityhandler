"""
Automation: IFTTT-style rules and reminders.
"""

from django.conf import settings
from django.db import models


class AutomationRule(models.Model):
    """If-This-Then-That style rule."""

    class TriggerType(models.TextChoices):
        TASK_COMPLETED = "task_completed", "Task completed"
        HABIT_CHECK_IN = "habit_check_in", "Habit checked in"
        TIME_OF_DAY = "time_of_day", "Time of day"
        DAILY = "daily", "Daily at time"

    class ActionType(models.TextChoices):
        CREATE_TASK = "create_task", "Create task"
        SEND_REMINDER = "send_reminder", "Send reminder"
        LOG_NOTE = "log_note", "Log note"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="automation_rules",
    )
    name = models.CharField(max_length=255)
    trigger_type = models.CharField(max_length=32, choices=TriggerType.choices)
    trigger_config = models.JSONField(default=dict, blank=True)
    action_type = models.CharField(max_length=32, choices=ActionType.choices)
    action_config = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Reminder(models.Model):
    """One-off or recurring reminder for the user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reminders",
    )
    title = models.CharField(max_length=255)
    remind_at = models.DateTimeField(db_index=True)
    recurring_rule = models.CharField(max_length=128, blank=True)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["remind_at"]

    def __str__(self):
        return self.title
