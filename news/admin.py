from django.contrib import admin

from news.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "title")