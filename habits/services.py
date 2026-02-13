"""
Habit streak calculation: consecutive days with at least one check-in.
"""
from datetime import timedelta

from django.utils import timezone

from .models import Habit, HabitCheckIn


def get_streak(habit: Habit) -> int:
    """Return current streak (consecutive days with completed check-in)."""
    today = timezone.now().date()
    streak = 0
    d = today
    while True:
        if HabitCheckIn.objects.filter(habit=habit, check_date=d, completed=True).exists():
            streak += 1
            d -= timedelta(days=1)
        else:
            break
    return streak
