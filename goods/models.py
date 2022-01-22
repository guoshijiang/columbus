# encoding=utf-8
from enum import Enum, unique

from django.db import models

from clbauth.models import AuthUser, UserAddress
from common.helpers import d0
from common.models import (
    Asset,
    BaseModel,
    BoolYesOrNoSelect,
    DecField,
)
from common.models import PayWaySelect
from marchant.models import Marchant

CalcWay = [(x, x) for x in ["件", "个", "斤"]]
ReturnExchange = [(x, x) for x in ["Return", "Exchange"]]


class GoodsCat(BaseModel):
    name = models.CharField(
        max_length=100,
        default="",
        verbose_name="分类名称",
    )
    is_active = models.BooleanField(
        default=True, verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "商品分类表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            "id": self.id,
            "user_name": self.name,
        }


class GoodsAttr(BaseModel):
    key = models.CharField(
        max_length=100,
        default="",
        verbose_name="属性Key",
    )
    value = models.CharField(
        max_length=100,
        default="",
        verbose_name="属性值",
    )
    is_active = models.BooleanField(
        default=True, verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "商品属性表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.key

    def as_dict(self):
        return {
            "id": self.id,
            "user_name": self.key,
        }


class GoodsImage(BaseModel):
    image = models.ImageField(
        upload_to="goods_img/%Y/%m/%d/",
        verbose_name="商品图片",
        blank=True,
        null=True,
    )
    mark = models.CharField(
        max_length=100,
        default="",
        verbose_name="图标备注",
    )
    is_active = models.BooleanField(
        default=True, verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "商品图片表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.image)

    def as_dict(self):
        return {
            "id": self.id,
            "user_name": self.mark,
        }


class GoodsSate(BaseModel):
    state = models.CharField(
        max_length=100,
        default="中国",
        verbose_name="产地名称",
    )
    is_active = models.BooleanField(
        default=True, verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "商品产地表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.state

    def as_dict(self):
        return {
            "id": self.id,
            "state": self.state,
        }


class Goods(BaseModel):
    merchant = models.ForeignKey(
        Marchant,
        related_name="marchant_goods_relate",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="商家",
    )
    goods_cat = models.ForeignKey(
        GoodsCat,
        related_name="goods_cat",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="商品分类",
    )
    goods_atrr = models.ManyToManyField(
        GoodsAttr,
        blank=True,
        null=True,
        verbose_name="商品属性",
    )
    goods_image = models.ManyToManyField(
        GoodsImage,
        blank=True,
        null=True,
        verbose_name="商品图片",
    )
    title = models.CharField(
        max_length=512,
        default="",
        verbose_name="商品标题",
    )
    goods_type = models.CharField(
        max_length=100,
        default="实体商品",
        verbose_name="商品类别",
    )
    name = models.CharField(
        max_length=512,
        default="",
        verbose_name="商品名称",
    )
    detail = models.CharField(
        max_length=512,
        default="",
        verbose_name="商品介绍",
    )
    logo = models.ForeignKey(
        GoodsImage,
        related_name="goods_logo_image",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="商品LOGO"
    )
    mark = models.CharField(
        max_length=512,
        default="",
        verbose_name="商品备注",
    )
    serveice = models.CharField(
        max_length=512,
        default="",
        verbose_name="服务说明",
    )
    calc_way = models.CharField(
        max_length=100,
        choices=CalcWay,
        default="件",
        verbose_name="计量方式",
    )
    pay_way = models.CharField(
        max_length=100,
        choices=PayWaySelect,
        default="All",
        verbose_name="支持支付的方式",
    )
    origin_state = models.ForeignKey(
        GoodsSate,
        related_name="goods_origin_state",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="商品产地",
    )
    total_amount = models.PositiveIntegerField(
        default=0, verbose_name="商品总量"
    )
    left_amount = models.PositiveIntegerField(
        default=100000, verbose_name="商品剩余量"
    )
    sell_nums = models.PositiveIntegerField(
        default=0, verbose_name="商品卖出量"
    )
    views = models.PositiveIntegerField(
        default=0, verbose_name="商品浏览次数"
    )
    return_goods_pc = models.CharField(
        max_length=1024,
        default="",
        verbose_name="退换货政策",
    )
    # 人民币价格
    price = DecField(
        default=d0, verbose_name="商品价格"
    )
    is_sale = models.CharField(
        max_length=100,
        choices=BoolYesOrNoSelect,
        default="Yes",
        verbose_name="商品上下架",
    )
    is_admin = models.CharField(
        max_length=100,
        choices=BoolYesOrNoSelect,
        default="Yes",
        verbose_name="商品是否代管",
    )
    is_active = models.BooleanField(
        default=True, verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "商品表"
        verbose_name_plural = "商品表"

    def __str__(self):
        return self.name

    def as_dict(self):
        return {"id": self.id}


@unique
class OrderStatus(Enum):
    NO_PAY = "NO_PAY"                    # 未支付
    PAY_SUCCESS = "PAY_SUCCESS"          # 支付成功, 等待发货
    PAY_FAIL = "PAY_FAIL"                # 支付失败
    SEND_GOODS = "SEND_GOODS"            # 已发货, 等待收货
    RECV_GOODS = "RECV_GOODS"            # 已经收货, 等待评价
    RETURN_GOODS = "RETURN_GOODS"        # 退货换货
    FINISH = "FINISH"                    # 已完成
    PAYWAYUSDT = "PAYWAYUSDT"            # 支付的 USDT
    PAYWAYBTC = "PAYWAYBTC"              # 支付的 BTC


# 订单表
class GoodsOrder(BaseModel):
    list_status = [
        status for status in OrderStatus
    ]
    status_choices: list = [
        (status.value, status.value)
        for status in OrderStatus
    ]

    goods = models.ForeignKey(
        Goods,
        related_name="goods_order_relate",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="商品",
    )
    merchant = models.ForeignKey(
        Marchant,
        related_name="marchant_goods_order_relate",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="商家",
    )
    user_address = models.ForeignKey(
        UserAddress,
        related_name="recive_goods_address_relate",
        on_delete=models.CASCADE,
        default="",
        verbose_name="收货地址",
    )
    goods_atrr = models.ManyToManyField(
        GoodsAttr,
        blank=True,
        null=True,
        verbose_name="商品属性",
    )
    status = models.CharField(
        max_length=100,
        choices=status_choices,
        default="Unpay",
        verbose_name="订单状态",
    )
    goods_name = models.CharField(
        max_length=512,
        default="",
        verbose_name="商品名称",
    )
    cny_amount = DecField(
        default=d0, verbose_name="总支付的人民币"
    )
    goods_price = DecField(
        default=d0, verbose_name="商品价格"
    )
    asset_cny_price = DecField(
        default=d0, verbose_name="支付时币种的人民币价格"
    )
    goods_detail = models.CharField(
        max_length=512,
        default="",
        verbose_name="商品介绍",
    )
    logo =  models.ForeignKey(
        GoodsImage,
        related_name="goods_order_logo_image",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="商品LOGO"
    )
    user = models.ForeignKey(
        AuthUser,
        related_name="buy_goods_user",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="购买商品的人",
    )
    buy_nums = models.PositiveIntegerField(
        default=1, verbose_name="购买数量"
    )
    pay_way = models.CharField(
        max_length=100,
        choices=PayWaySelect,
        default="件",
        verbose_name="计量方式",
    )
    pay_asset = models.ForeignKey(
        Asset,
        null=False,
        verbose_name="支付币种",
        on_delete=models.CASCADE,
    )
    pay_asset_cny_price = DecField(
        default=d0, verbose_name="支付时资产的人民币价格"
    )
    pay_coin_amount = DecField(
        default=d0, verbose_name="支付的币的数量"
    )
    order_number = models.CharField(
        max_length=512,
        default="",
        verbose_name="订单号",
    )
    logistics = models.CharField(
        max_length=512,
        default="",
        verbose_name="物流公司",
    )
    express_number = models.CharField(
        max_length=512,
        default="",
        verbose_name="快递运单号",
    )
    ret_logistics = models.CharField(
        max_length=512,
        default="",
        verbose_name="退货物流公司",
    )
    ret_ship_number = models.CharField(
        max_length=512,
        default="",
        verbose_name="退货运单号",
    )

    failure_reason = models.CharField(
        max_length=512,
        default="",
        verbose_name="失败原因",
    )
    pay_at = models.CharField(
        max_length=512,
        default="",
        verbose_name="支付时间",
    )
    deal_at = models.CharField(
        max_length=512,
        default="",
        verbose_name="处理时间",
    )
    is_cancle = models.CharField(
        max_length=100,
        choices=BoolYesOrNoSelect,
        default="No",
        verbose_name="是否退换货",
    )
    is_comment = models.CharField(
        max_length=100,
        choices=BoolYesOrNoSelect,
        default="No",
        verbose_name="是否评价价",
    )
    is_settle = models.CharField(
        max_length=100,
        choices=BoolYesOrNoSelect,
        default="No",
        verbose_name="是否结算",
    )
    is_active = models.BooleanField(
        default=True, verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "商品订单表"
        verbose_name_plural = "商品订单表"

    def __str__(self):
        return self.order_number

    def as_dict(self):
        return {"id": self.id}


class OrederReturnStatus(Enum):
    RETURN_GOODS  = "RETURN_GOODS"             # 买家发起退换货
    CANCLE_RETURN_GOODS = "CANCLE_RETURN_GOODS"  # 买家发起退换货
    RETURN_SELLER_RJT = "RETURN_SELLER_RJT"    # 卖家拒绝
    RETURN_SELLER_ACPT = "RETURN_SELLER_ACPT"  # 卖家同意, 并联系买家处理，如果卖家已发货，需要买家将货邮寄回来
    BUYER_APPOVAL = "BUYER_APPOVAL"            # 买家申诉, 平台处理
    APPOVAL_FAIL = "APPOVAL_FAIL"              # 订单申诉失败
    APPOVAL_SUCCESS = "APPOVAL_SUCCESS"        # 订单申诉成功
    BUYER_SEND_GOODS = "BUYER_SEND_GOODS"      # 买家已发货, 卖家等待收货
    BUYER_RECV_GOODS = "BUYER_RECV_GOODS"      # 买家已发货
    SELLER_RECV_GOODS = "SELLER_RECV_GOODS"    # 卖家已经收到货,
    SELLER_SEND_GOODS = "SELLER_SEND_GOODS"    # 卖家已发货，买家等待收货
    SELLER_RETURN_MNY = "SELLER_RETURN_MNY"    # 卖家已经退款


# 退换货订单流程表
class OrederReturn(BaseModel):
    list_status = [
        status for status in OrderStatus
    ]
    status_choices: list = [
        (status.value, status.value)
        for status in OrederReturnStatus
    ]

    order = models.ForeignKey(
        GoodsOrder,
        related_name="goods_order_return",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="订单",
    )
    ret_goods_rs = models.CharField(
        max_length=512,
        default="",
        verbose_name="退货原因",
    )
    ret_pay_rs = models.CharField(
        max_length=512,
        default="",
        verbose_name="商家拒绝原因",
    )
    qs_describe = models.CharField(
        max_length=512,
        default="",
        verbose_name="问题描述",
    )
    qs_img_one = models.ImageField(
        upload_to="order/%Y/%m/%d/",
        verbose_name="问题图片1",
        blank=True,
        null=True,
    )
    qs_img_two = models.ImageField(
        upload_to="order/%Y/%m/%d/",
        verbose_name="问题图片2",
        blank=True,
        null=True,
    )
    qs_img_three = models.ImageField(
        upload_to="order/%Y/%m/%d/",
        verbose_name="问题图片3",
        blank=True,
        null=True,
    )
    adjust_content = models.CharField(
        max_length=5120,
        default="",
        verbose_name="申述描述",
    )
    adjust_reason = models.CharField(
        max_length=5120,
        default="",
        verbose_name="申述描述",
    )
    vectory_id = models.PositiveIntegerField(
        default=1, verbose_name="申诉胜出方"
    )
    fail_id = models.PositiveIntegerField(
        default=1, verbose_name="申诉失败方"
    )
    process = models.CharField(
        max_length=100,
        choices=status_choices,
        default="RETURN_GOODS",
        verbose_name="订单状态",
    )
    ret_order_status = models.CharField(
        max_length=100,
        default="",
        verbose_name="退换货前订单状态",
    )
    is_send_goods = models.CharField(
        max_length=100,
        choices=BoolYesOrNoSelect,
        default="No",
        verbose_name="是否已发货物",
    )
    fund_ret = models.CharField(
        max_length=100,
        choices=ReturnExchange,
        default="Return",
        verbose_name="退货换货",
    )
    left_time = models.CharField(
        max_length=512,
        default="",
        verbose_name="剩余处理时长",
    )
    deal_time = models.CharField(
        max_length=512,
        default="",
        verbose_name="处理时间",
    )
    is_active = models.BooleanField(
        default=True, verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "订单退货流程表"
        verbose_name_plural = "订单退货流程表"

    def __str__(self):
        return self.ret_goods_rs

    def as_dict(self):
        return {"id": self.id}


class GoodsComment(BaseModel):
    goods = models.ForeignKey(
        Goods,
        related_name="goods_relate_comment",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="商品",
    )
    user = models.ForeignKey(
        AuthUser,
        related_name="goods_comment_user",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="评论人",
    )
    merchant = models.ForeignKey(
        Marchant,
        related_name="goods_marchant_comment",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="所属商家",
    )
    quality_star = models.PositiveIntegerField(
        default=0, verbose_name="评论的质量星级"
    )
    service_star = models.PositiveIntegerField(
        default=0, verbose_name="服务评论星级"
    )
    trade_star = models.PositiveIntegerField(
        default=0, verbose_name="交易评论星级"
    )
    content = models.CharField(
        max_length=512,
        default="",
        verbose_name="评论内容",
    )

    class Meta:
        verbose_name = "商品评价表"
        verbose_name_plural = "商品评价表"

    def __str__(self):
        return self.content

    def as_dict(self):
        return {"id": self.id}


class GoodsCollect(BaseModel):
    user = models.ForeignKey(
        AuthUser,
        related_name="goods_collect_user",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="用户",
    )
    goods = models.ForeignKey(
        Goods,
        related_name="goods_collect_db",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="收藏的商品",
    )
    is_active = models.BooleanField(
        default=True, verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "商品收藏表"
        verbose_name_plural = "商品收藏表"

    def __str__(self):
        return ""

    def as_dict(self):
        return {"id": self.id}
