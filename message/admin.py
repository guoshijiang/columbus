from django.contrib import admin
from message.models import (
    Message, HelpDesk, MsgFriends
)


@admin.register(HelpDesk)
class HelpDeskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "content")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "title")


@admin.register(MsgFriends)
class MsgFriendsAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "created_at")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "msg_type", "msg_content")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "msg_type")

