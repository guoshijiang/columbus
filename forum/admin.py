from django.contrib import admin

from forum.models import FormCat, FormTopic, FormCommentReply, Form


@admin.register(FormCat)
class FormCatAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "name")


@admin.register(FormTopic)
class FormTopicAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "name")


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("id", "content")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "content")


@admin.register(FormCommentReply)
class FormCommentReplyAdmin(admin.ModelAdmin):
    list_display = ("id", "content")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "content")