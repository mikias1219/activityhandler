from rest_framework import serializers

from .models import Habit, HabitCheckIn


class HabitCheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitCheckIn
        fields = ["id", "check_date", "completed", "notes", "created_at"]
        read_only_fields = ["created_at"]


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            "id",
            "name",
            "target_frequency",
            "target_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class HabitWithStreakSerializer(HabitSerializer):
    current_streak = serializers.IntegerField(read_only=True)

    class Meta(HabitSerializer.Meta):
        fields = HabitSerializer.Meta.fields + ["current_streak"]
