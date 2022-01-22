from django.contrib import admin

from goods.models import (
    Goods,
    GoodsAttr,
    GoodsCat,
    GoodsImage,
    GoodsSate,
    GoodsOrder,
    OrederReturn,
    GoodsComment,
    GoodsCollect
)



@admin.register(GoodsAttr)
class GoodsAttrAdmin(admin.ModelAdmin):
    list_display = ("id", "key", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "key")


@admin.register(GoodsSate)
class GoodsSateAdmin(admin.ModelAdmin):
    list_display = ("id", "state", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "state")


@admin.register(GoodsImage)
class GoodsSateAdmin(admin.ModelAdmin):
    list_display = ("id", "mark", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "mark")


@admin.register(GoodsCat)
class GoodsSateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "name")


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "name")


@admin.register(GoodsOrder)
class GoodsOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "order_number", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "order_number")


@admin.register(OrederReturn)
class GoodsOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "ret_goods_rs", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "ret_goods_rs")


@admin.register(GoodsComment)
class GoodsCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "content")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "content")


@admin.register(GoodsCollect)
class GoodsCollectAdmin(admin.ModelAdmin):
    list_display = ("id", "is_active")
    list_per_page = 50
    ordering = ("-created_at",)
    list_display_links = ("id", "is_active")
