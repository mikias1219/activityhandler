"""Serve the LifeOS web UI (templates). Auth is via JWT in localStorage (frontend)."""

from django.shortcuts import redirect, render


def login_view(request):
    return render(request, "auth/login.html")


def register_view(request):
    return render(request, "auth/register.html")


def password_reset_view(request):
    return render(request, "auth/password_reset.html")


def password_reset_confirm_view(request):
    return render(
        request,
        "auth/password_reset_confirm.html",
        {
            "uid": request.GET.get("uid", ""),
            "token": request.GET.get("token", ""),
        },
    )


def dashboard_view(request):
    return render(request, "app/dashboard.html", {"current_page": "dashboard"})


def tasks_view(request):
    return render(request, "app/tasks.html", {"current_page": "tasks"})


def habits_view(request):
    return render(request, "app/habits.html", {"current_page": "habits"})


def finance_view(request):
    return render(request, "app/finance.html", {"current_page": "finance"})


def automation_view(request):
    return render(request, "app/automation.html", {"current_page": "automation"})


def index_view(request):
    return redirect("web:dashboard")
