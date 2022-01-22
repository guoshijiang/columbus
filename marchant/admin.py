from django.contrib import admin

from marchant.models import (
    Marchant,
    MarchantConfig,
    MarchantStat,
    MarchantCollect,
    MarchantOrderFlow,
    MarchantOpenRecord,
    MarchantBackList
)


@admin.register(Marchant)
class MarchantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "name")


@admin.register(MarchantConfig)
class MarchantConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "btc_amount", "usdt_amount", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "btc_amount")


@admin.register(MarchantStat)
class MarchantStatAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "created_at")


@admin.register(MarchantCollect)
class MarchantCollectAdmin(admin.ModelAdmin):
    list_display = ("id", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "is_active")


@admin.register(MarchantOrderFlow)
class MarchantOrderFlowCollectAdmin(admin.ModelAdmin):
    list_display = ("id", "order_id", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "order_id")


@admin.register(MarchantOpenRecord)
class MarchantOpenRecordCollectAdmin(admin.ModelAdmin):
    list_display = ("id", "pay_coin_amount", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "pay_coin_amount")



@admin.register(MarchantBackList)
class MarchantBackListCollectAdmin(admin.ModelAdmin):
    list_display = ("id", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "is_active")