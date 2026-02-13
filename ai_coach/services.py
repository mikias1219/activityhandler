"""
AI Coach: rule-based suggestions + optional Azure OpenAI / OpenAI API.
"""

from datetime import date
from typing import Any

from django.conf import settings


def get_what_to_do_now(user) -> dict[str, Any]:
    """
    "What should I do now?" — combines tasks due today, overdue tasks,
    and habit check-ins due. Optional LLM can enhance with natural language.
    """
    from habits.models import Habit, HabitCheckIn
    from productivity.models import Task

    today = date.today()
    suggestions: list[dict[str, Any]] = []

    # Overdue tasks
    overdue = Task.objects.filter(
        user=user,
        due_date__lt=today,
        status__in=[Task.Status.TODO, Task.Status.IN_PROGRESS],
    ).order_by("due_date", "priority")[:5]
    for t in overdue:
        suggestions.append(
            {
                "type": "overdue_task",
                "priority": "high",
                "title": t.title,
                "id": t.pk,
                "due_date": str(t.due_date),
            }
        )

    # Today's tasks not done
    today_tasks = Task.objects.filter(
        user=user,
        due_date=today,
        status__in=[Task.Status.TODO, Task.Status.IN_PROGRESS],
    ).order_by("priority", "created_at")[:5]
    for t in today_tasks:
        suggestions.append({"type": "task", "priority": "medium", "title": t.title, "id": t.pk})

    # Habits not checked in today
    for habit in Habit.objects.filter(user=user):
        if not HabitCheckIn.objects.filter(habit=habit, check_date=today).exists():
            suggestions.append(
                {"type": "habit", "priority": "medium", "title": habit.name, "id": habit.pk}
            )

    msg = _enhance_with_llm(suggestions) if suggestions else None
    return {
        "suggestions": suggestions[:10],
        "message": msg
        or (
            "You're all set for now. Consider adding a task or habit."
            if not suggestions
            else "Here are your priorities."
        ),
    }


def _enhance_with_llm(suggestions: list) -> str | None:
    """Optional: call Azure OpenAI or OpenAI for a short motivational line. Returns None if no key configured."""
    api_key = getattr(settings, "OPENAI_API_KEY", None) or getattr(
        settings, "AZURE_OPENAI_API_KEY", None
    )
    if not api_key:
        return None
    try:
        import openai

        client = getattr(openai, "AzureOpenAI", openai.OpenAI)
        if getattr(settings, "AZURE_OPENAI_ENDPOINT", None):
            client = openai.AzureOpenAI(
                api_key=api_key,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                api_version=getattr(settings, "AZURE_OPENAI_API_VERSION", "2024-02-01"),
            )
        else:
            client = openai.OpenAI(api_key=api_key)
        titles = [s["title"] for s in suggestions[:5]]
        r = client.chat.completions.create(
            model=getattr(settings, "OPENAI_DEPLOYMENT_OR_MODEL", "gpt-4o-mini"),
            messages=[
                {
                    "role": "user",
                    "content": f"One short motivating sentence (under 15 words) for someone who has these to do: {titles}",
                }
            ],
            max_tokens=50,
        )
        if r.choices:
            return (r.choices[0].message.content or "").strip()
    except Exception:
        pass
    return None
