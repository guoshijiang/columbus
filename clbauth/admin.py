from django.contrib import admin

from clbauth.models import (
    Asset,
    AuthUser,
    UserAddress,
    UserWallet,
    WalletRecord,
    TansRecord
)

@admin.register(AuthUser)
class AuthUserAdmin(admin.ModelAdmin):
    list_display = ("id", "user_name", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "user_name")


@admin.register(UserWallet)
class AuthUserAdmin(admin.ModelAdmin):
    list_display = ("id", "address", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "address")


@admin.register(WalletRecord)
class WalletRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "tx_hash", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "tx_hash")


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user_name", "address", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "user_name")


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "name")


@admin.register(TansRecord)
class TansRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "is_active")

