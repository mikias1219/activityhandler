from django.urls import path

from .views import TaskDetailView, TaskListCreateView, TaskTodayView

urlpatterns = [
    path("tasks/today/", TaskTodayView.as_view(), name="tasks-today"),
    path("tasks/", TaskListCreateView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
]
