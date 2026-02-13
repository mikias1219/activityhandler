"""
Core views: health check.
"""
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.utils.decorators import method_decorator


@require_GET
@csrf_exempt
def health(request) -> JsonResponse:
    """Health check for load balancer and monitoring."""
    return JsonResponse({"status": "ok", "service": "lifeos"})
