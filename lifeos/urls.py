"""
LifeOS URL configuration.
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from core.urls import urlpatterns as core_urls

API_V1 = [
    path("", include("users.urls")),
    path("", include("productivity.urls")),
    path("", include("habits.urls")),
    path("", include("finance.urls")),
    path("ai/", include("ai_coach.urls")),
    path("automation/", include("automation.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("web.urls")),
    path("api/", include(core_urls)),
    path("api/v1/", include(API_V1)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
