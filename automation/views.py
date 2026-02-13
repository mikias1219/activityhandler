from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import AutomationRule, Reminder
from .serializers import AutomationRuleSerializer, ReminderSerializer


class AutomationRuleListCreateView(generics.ListCreateAPIView):
    serializer_class = AutomationRuleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AutomationRule.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AutomationRuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AutomationRuleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AutomationRule.objects.filter(user=self.request.user)


class ReminderListCreateView(generics.ListCreateAPIView):
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user).order_by("remind_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReminderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)
