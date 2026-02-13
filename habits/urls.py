from django.urls import path

from .views import (
    HabitCheckInDetailView,
    HabitCheckInListCreateView,
    HabitDetailView,
    HabitListCreateView,
    HabitStreakView,
)

urlpatterns = [
    path("habits/", HabitListCreateView.as_view(), name="habit-list"),
    path("habits/<int:pk>/", HabitDetailView.as_view(), name="habit-detail"),
    path("habits/<int:habit_pk>/check-ins/", HabitCheckInListCreateView.as_view(), name="habit-check-ins"),
    path("habits/<int:habit_pk>/check-ins/<int:pk>/", HabitCheckInDetailView.as_view(), name="habit-check-in-detail"),
    path("habits/<int:habit_pk>/streak/", HabitStreakView.as_view(), name="habit-streak"),
]
