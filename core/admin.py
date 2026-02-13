from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["user", "request_method", "request_path", "created_at"]
    list_filter = ["request_method", "created_at"]
    search_fields = ["request_path", "user__email"]
    readonly_fields = ["user", "action", "resource_type", "resource_id", "request_path", "request_method", "ip_address", "created_at"]
    date_hierarchy = "created_at"
