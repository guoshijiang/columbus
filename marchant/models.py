# encoding=utf-8

from django.db import models

from clbauth.models import AuthUser
from common.helpers import d0
from common.models import (
    Asset,
    BaseModel,
    BoolYesOrNoSelect,
    DecField,
)
from common.models import PayWaySelect

MarchantConfigSelect = [
    (x, x) for x in ["Marchant", "Other"]
]


class Marchant(BaseModel):
    user = models.ForeignKey(
        AuthUser,
        related_name="marchant_user_relate",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="用户",
    )
    logo = models.ImageField(
        upload_to="marchant/%Y/%m/%d/",
        verbose_name="商家LOGO",
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="商家名称",
    )
    introduce = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="商家介绍",
    )
    detail = models.CharField(
        max_length=1024,
        default="",
        blank=True,
        null=True,
        verbose_name="商家详细说明",
    )
    goods_num = models.PositiveIntegerField(
        default=0,
        verbose_name="商家商品个数"
    )
    settle_percent = DecField(
        default=d0,
        verbose_name="商家和平台结算比例"
    )
    shop_level = models.PositiveIntegerField(
        default=0,
        verbose_name="商家等级"
    )
    shop_score = models.CharField(
        max_length=100,
        default="0",
        blank=True,
        null=True,
        verbose_name="商家评分",
    )
    month_sell_num = models.PositiveIntegerField(
        default=0,
        verbose_name="本月销售量"
    )
    month_sell_amount = DecField(
        default=d0,
        verbose_name="本月销售金额"
    )
    total_sell_num = models.PositiveIntegerField(
        default=0,
        verbose_name="总销售量"
    )
    total_sell_amount = DecField(
        default=d0,
        verbose_name="总的销售金额"
    )
    adjust_victor = models.PositiveIntegerField(
        default=0,
        verbose_name="调解成功次数"
    )
    adjust_fail = models.PositiveIntegerField(
        default=0,
        verbose_name="调解失败次数"
    )
    is_active = models.BooleanField(
        default=True, verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "商家表"
        verbose_name_plural = "商家表"

    def __str__(self):
        return self.name

    def as_dict(self):
        return {"id": self.id}


class MarchantCollect(BaseModel):
    user = models.ForeignKey(
        AuthUser,
        related_name="marchant_collect_user",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="用户",
    )
    marchant = models.ForeignKey(
        Marchant,
        related_name="marchant_collect_relate",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="收藏的商家",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "商家收藏表"
        verbose_name_plural = "商家收藏表"

    def __str__(self):
        pass

    def as_dict(self):
        return {"id": self.id}


class MarchantConfig(BaseModel):
    btc_amount = DecField(
        default=d0,
        verbose_name="开通商家所需 BTC 个数"
    )
    eth_amount = DecField(
        default=d0,
        verbose_name="开通商家所需 ETH 个数"
    )
    usdt_amount = DecField(
        default=d0,
        verbose_name="开通商家所需 USDT 个数"
    )
    config_type = models.CharField(
        max_length=100,
        choices=MarchantConfigSelect,
        default="Marchant",
        blank=True,
        null=True,
        verbose_name="配置类别",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "商家配置表"
        verbose_name_plural = "商家配置表"

    def as_dict(self):
        return {"id": self.id}


class MarchantOpenRecord(BaseModel):
    user = models.ForeignKey(
        AuthUser,
        related_name="marchant_open_user_record_relate",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="用户",
    )
    marchant = models.ForeignKey(
        Marchant,
        related_name="marchant_open_marchant",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="收藏的商家",
    )
    pay_coin_amount = DecField(
        default=d0,
        verbose_name="支付的币种数量"
    )
    pay_way = models.CharField(
        max_length=100,
        choices=PayWaySelect,
        default="BTC",
        blank=True,
        null=True,
        verbose_name="配置类别",
    )
    pay_at = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="支付时间",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "开通商家记录表"
        verbose_name_plural = "开通商家记录表"

    def __str__(self):
        return ""

    def as_dict(self):
        return {"id": self.id}


class MarchantOrderFlow(BaseModel):
    marchant = models.ForeignKey(
        Marchant,
        related_name="marchant_order_flow_relate",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="商家",
    )
    order_id = models.PositiveIntegerField(
        default=0,
        verbose_name="订单ID"
    )
    asset = models.ForeignKey(
        Asset,
        related_name="marchant_flow_asset_relate",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="订单",
    )
    coin_amount = DecField(
        default=d0,
        verbose_name="币的数量"
    )
    is_valid = models.CharField(
        max_length=100,
        choices=BoolYesOrNoSelect,
        default="No",
        blank=True,
        null=True,
        verbose_name="是否有效数据",
    )
    is_stat = models.CharField(
        max_length=100,
        choices=BoolYesOrNoSelect,
        default="No",
        blank=True,
        null=True,
        verbose_name="是否已经统计",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否有效"
    )

    class Meta:
        verbose_name = "商家流水表"
        verbose_name_plural = "商家流水表"

    def __str__(self):
        return ""

    def as_dict(self):
        return {"id": self.id}


class MarchantStat(BaseModel):
    marchant = models.ForeignKey(
        Marchant,
        related_name="marchant_data_stat_mct",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="商家",
    )
    serice_best = models.PositiveIntegerField(
        default=0,
        verbose_name="服务好评"
    )
    service_good = models.PositiveIntegerField(
        default=0,
        verbose_name="服务中评"
    )
    service_bad = models.PositiveIntegerField(
        default=0,
        verbose_name="服务差评"
    )
    service_avg = DecField(
        default=d0,
        verbose_name="服务评论星率"
    )
    service_num = models.PositiveIntegerField(
        default=0,
        verbose_name="服务星星数量"
    )
    trade_best = models.PositiveIntegerField(
        default=0,
        verbose_name="交易好评"
    )
    trade_good = models.PositiveIntegerField(
        default=0,
        verbose_name="交易中评"
    )
    trade_bad = models.PositiveIntegerField(
        default=0,
        verbose_name="交易差评"
    )
    trade_avg = DecField(
        default=d0,
        verbose_name="交易评论星率"
    )
    trade_num = models.PositiveIntegerField(
        default=0,
        verbose_name="交易星星数量"
    )
    quality_best = models.PositiveIntegerField(
        default=0,
        verbose_name="质量好评"
    )
    quality_good = models.PositiveIntegerField(
        default=0,
        verbose_name="质量中评"
    )
    quality_bad = models.PositiveIntegerField(
        default=0,
        verbose_name="质量差评"
    )
    quality_avg = DecField(
        default=d0,
        verbose_name="质量评论星率"
    )
    quality_num = models.PositiveIntegerField(
        default=0,
        verbose_name="质量评论星星数量"
    )
    total_cmt_num = models.PositiveIntegerField(
        default=0,
        verbose_name="总评价星星数量"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "商家数据统计表"
        verbose_name_plural = "商家数据统计表"

    def __str__(self):
        return ""

    def as_dict(self):
        return {"id": self.id}


class MarchantBackList(BaseModel):
    user = models.ForeignKey(
        AuthUser,
        related_name="marchant_blacklist_user",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="用户",
    )
    marchant = models.ForeignKey(
        Marchant,
        related_name="marchant_blacklist_mct_relate",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="黑名单商家",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "屏蔽商家表"
        verbose_name_plural = "屏蔽商家表"

    def __str__(self):
        return ""

    def as_dict(self):
        return {"id": self.id}
