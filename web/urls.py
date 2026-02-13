from django.urls import path

from . import views

app_name = "web"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("password-reset/", views.password_reset_view, name="password_reset"),
    path(
        "password-reset/confirm/", views.password_reset_confirm_view, name="password_reset_confirm"
    ),
    path("app/", views.dashboard_view, name="dashboard"),
    path("app/tasks/", views.tasks_view, name="tasks"),
    path("app/habits/", views.habits_view, name="habits"),
    path("app/finance/", views.finance_view, name="finance"),
    path("app/automation/", views.automation_view, name="automation"),
]
