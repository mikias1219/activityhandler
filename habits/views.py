from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Habit, HabitCheckIn
from .serializers import HabitCheckInSerializer, HabitSerializer
from .services import get_streak


class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitCheckInListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitCheckInSerializer
    permission_classes = [IsAuthenticated]

    def get_habit(self):
        return Habit.objects.get(pk=self.kwargs["habit_pk"], user=self.request.user)

    def get_queryset(self):
        habit = self.get_habit()
        return HabitCheckIn.objects.filter(habit=habit).order_by("-check_date")

    def perform_create(self, serializer):
        habit = self.get_habit()
        serializer.save(habit=habit, user=self.request.user)


class HabitCheckInDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitCheckInSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HabitCheckIn.objects.filter(
            habit_id=self.kwargs["habit_pk"],
            habit__user=self.request.user,
        )


class HabitStreakView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, habit_pk: int) -> Response:
        habit = Habit.objects.filter(pk=habit_pk, user=request.user).first()
        if not habit:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"habit_id": habit.pk, "current_streak": get_streak(habit)})
