from django.contrib import admin
from .models import Habit, HabitCheckIn


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "target_frequency", "target_count", "created_at"]
    list_filter = ["target_frequency"]
    search_fields = ["name"]
    raw_id_fields = ["user"]


@admin.register(HabitCheckIn)
class HabitCheckInAdmin(admin.ModelAdmin):
    list_display = ["habit", "user", "check_date", "completed", "created_at"]
    list_filter = ["completed", "check_date"]
    raw_id_fields = ["habit", "user"]
    date_hierarchy = "check_date"
