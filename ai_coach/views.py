"""
AI Coach API: what should I do now, weekly summary (stub).
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import get_what_to_do_now


class WhatToDoNowView(APIView):
    """GET /api/v1/ai/what-to-do-now/ — suggestions based on tasks and habits."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = get_what_to_do_now(request.user)
        return Response(data)
