from django.contrib import admin
from backend.models import AdminUser


@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "name")
