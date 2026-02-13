from django.urls import path

from .views import (
    AutomationRuleDetailView,
    AutomationRuleListCreateView,
    ReminderDetailView,
    ReminderListCreateView,
)

urlpatterns = [
    path("rules/", AutomationRuleListCreateView.as_view(), name="automation-rule-list"),
    path("rules/<int:pk>/", AutomationRuleDetailView.as_view(), name="automation-rule-detail"),
    path("reminders/", ReminderListCreateView.as_view(), name="reminder-list"),
    path("reminders/<int:pk>/", ReminderDetailView.as_view(), name="reminder-detail"),
]
