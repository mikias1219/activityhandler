from django.contrib import admin
from .models import AutomationRule, Reminder


@admin.register(AutomationRule)
class AutomationRuleAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "trigger_type", "action_type", "is_active", "created_at"]
    list_filter = ["trigger_type", "action_type", "is_active"]
    raw_id_fields = ["user"]


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "remind_at", "is_sent", "created_at"]
    list_filter = ["is_sent"]
    raw_id_fields = ["user"]
    date_hierarchy = "remind_at"
