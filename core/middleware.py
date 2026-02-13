"""
Audit logging middleware — logs authenticated API requests.
"""
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class AuditLoggingMiddleware(MiddlewareMixin):
    """Log API requests for audit (skips health, static, etc.)."""

    def process_request(self, request) -> None:
        path = request.path
        if not getattr(settings, "AUDIT_LOG_ENABLED", True):
            return
        skip_paths = getattr(settings, "AUDIT_LOG_SKIP_PATHS", [])
        if any(path.startswith(p) for p in skip_paths):
            return
        if not path.startswith("/api/"):
            return
        # Defer log write to process_response so we have response status
        request._audit_path = path
        request._audit_method = request.method
        request._audit_user = getattr(request, "user", None) if request.user.is_authenticated else None

    def process_response(self, request, response) -> None:
        if not getattr(request, "_audit_path", None):
            return response
        if not getattr(settings, "AUDIT_LOG_ENABLED", True):
            return response
        try:
            from core.models import AuditLog

            AuditLog.objects.create(
                user=request._audit_user,
                action=f"{request._audit_method} {request._audit_path}",
                resource_type="",
                resource_id="",
                request_path=request._audit_path,
                request_method=request._audit_method,
                ip_address=self._get_client_ip(request),
            )
        except Exception:
            pass  # Never break response for audit failure
        return response

    @staticmethod
    def _get_client_ip(request) -> str | None:
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            return xff.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
