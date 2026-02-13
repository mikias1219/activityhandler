from django.urls import path

from .views import WhatToDoNowView

urlpatterns = [
    path("what-to-do-now/", WhatToDoNowView.as_view(), name="ai-what-to-do-now"),
]
