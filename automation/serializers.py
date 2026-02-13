from rest_framework import serializers

from .models import AutomationRule, Reminder


class AutomationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutomationRule
        fields = [
            "id", "name", "trigger_type", "trigger_config",
            "action_type", "action_config", "is_active",
            "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ["id", "title", "remind_at", "recurring_rule", "is_sent", "created_at"]
        read_only_fields = ["is_sent", "created_at"]
