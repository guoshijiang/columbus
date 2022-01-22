# encoding=utf-8

import time
from decimal import Decimal

import pytz
from django import template
from django.conf import settings
from common.models import Asset
from common.helpers import d0, dec


register = template.Library()


@register.filter(name="hdatetime")
def repr_datetime(value) -> str:
    if not value:
        return ""
    tz = pytz.timezone(settings.TIME_ZONE)
    return value.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")


@register.filter(name="cn_hdatetime")
def cn_hdatetime(value) -> str:
    if not value:
        return ""
    tz = pytz.timezone(settings.TIME_ZONE)
    return value.astimezone(tz).strftime("%m月%d日 %H:%M")


@register.filter(name="keep_two_decimal_places")
def ktd_places(value):
    if value in ["", None, "None", 0, d0]:
        return "0"
    dec_value = Decimal(value).quantize(Decimal("0.0000"))
    return (
        dec_value.to_integral()
        if dec_value == dec_value.to_integral()
        else dec_value.normalize()
    )


@register.filter(name="eth_price")
def eth_price(value):
    if value in ["", None, "None", 0, d0]:
        return "0.00"
    eth_asset = Asset.objects.filter(name="ETH").first()
    goods_eth_p = value / dec(eth_asset.cny_price)
    return goods_eth_p


@register.filter(name="usdt_price")
def usdt_price(value):
    if value in ["", None, "None", 0, d0]:
        return "0.00"
    usdt_asset = Asset.objects.filter(name="USDT").first()
    goods_usdt_p = value / dec(usdt_asset.cny_price)
    return goods_usdt_p


@register.filter(name="user_order_status")
def user_order_status(value):
    return {
        'NO_PAY': '未支付',
        'PAY_SUCCESS': '等待发货',
        'SEND_GOODS': '等待收货',
        'RECV_GOODS': '等待评价',
        'RETURN_GOODS': '发起退货换货',
        'CANCLE_RETURN_GOODS': '取消退货换货',
        'RETURN_SELLER_RJT': '卖家拒绝',
        'RETURN_SELLER_ACPT': '卖家同意',
        'BUYER_APPOVAL': '买家申诉',
        'APPOVAL_FAIL': '买家申诉失败',
        'APPOVAL_SUCCESS': '订单申诉成功',
        'BUYER_SEND_GOODS': '买家已发货, 卖家等待收货',
        'BUYER_RECV_GOODS': '买家已发货',
        'SELLER_RECV_GOODS': '卖家已经收到货',
        'SELLER_SEND_GOODS': '卖家已发货，买家等待收货',
        'SELLER_RETURN_MNY': '卖家已退款',
        "FINISH": "已完成"
    }.get(value, '')


@register.filter(name="marchant_order_status")
def marchant_order_status(value):
    return {
        'NO_PAY': '待付款',
        'PAY_SUCCESS': '等待发货',
        'SEND_GOODS': '您已发货，等待客户收货',
        'RECV_GOODS': '客户已收货',
        'RETURN_GOODS': '退货换货',
        'RETURN_SELLER_RJT': '您已拒绝退货, 用户可能会发起申述',
        'RETURN_SELLER_ACPT': '您已同意退货，如果已发货，等待卖家将货物邮寄给您，再退款',
        'BUYER_APPOVAL': '用户发起申诉, 等待平台处理',
        'APPOVAL_SUCCESS': '订单申诉成功',
        'SELLER_RETURN_MNY': '您已退款，该订单已经完成',
        "FINISH": "已完成"
    }.get(value, '')


@register.filter(name="wallet_record_status")
def wallet_record_status(value):
    return {
        'Checking': '审核中(未锁定)',
        'Trading': '交易中',
        'SendOut': '已发出',
        'Success': '成功',
        'Fail': '失败',
        'CheckPass': '审核通过',
        'CheckRefuse': '审核拒绝',

    }.get(value, '')


@register.filter(name="helpdesk_handle")
def helpdesk_handle(value):
    return {
        'UnHandle': '未处理',
        'Handling': '处理中',
        'Handled': '已处理'
    }.get(value, '')


@register.filter(name="trans_way")
def trans_way(value):
    return {
        'Input': '收入',
        'Output': '支出',
    }.get(value, '')