# encoding=utf-8

from django.db import models

from common.helpers import d0, dec
from common.models import (
    Asset,
    BaseModel,
    BoolYesOrNoSelect,
    DecField,
)

WithdrawDeposit = [
    (x, x) for x in ["Withdraw", "Deposit", "Transfer"]
]

TransWay = [
    (x, x) for x in ["Input", "Output"]
]

'''
Checking:    审核中(未锁定)
Trading:     交易中 
SendOut:     已发出 
Success:     成功 
Fail:        失败  
CheckPass:   审核通过 
CheckRefuse: 审核拒绝
'''
WalletStatus = [
    (x, x) for x in ["Checking", "Checked", "Trading", "SendOut", "Success", "Fail", "CheckPass", "CheckRefuse"]
]
'''
Input: 收入
Output: 支出
'''
TransRecordStatus = [
    (x, x) for x in ["Output", "Input"]
]

class AuthUser(BaseModel):
    user_name = models.CharField(
        max_length=100,
        default="columbos",
        verbose_name="用户名",
    )
    user_pho = models.ImageField(
        upload_to="user_img/%Y/%m/%d/",
        verbose_name="文章图片",
        blank=True,
        null=True,
    )
    password = models.CharField(
        max_length=100,
        default="",
        verbose_name="用户密码",
    )
    pin_code = models.CharField(
        max_length=100,
        default="",
        verbose_name="Pin码",
    )
    login_count = models.PositiveIntegerField(
        default=0,
        verbose_name="登陆次数"
    )
    token = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="用户token",
    )
    is_merchant = models.CharField(
        max_length=100,
        choices=BoolYesOrNoSelect,
        default="No",
        db_index=True,
        verbose_name="是不是商家",
    )
    member_level = models.PositiveIntegerField(
        default=0,
        verbose_name="登陆级别"
    )
    user_private_key = models.CharField(
        max_length=4096,
        default="",
        blank=True,
        null=True,
        verbose_name="私钥",
    )
    user_public_key = models.CharField(
        max_length=4096,
        default="",
        blank=True,
        null=True,
        verbose_name="公钥",
    )
    factor = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="Pin码",
    )
    is_open = models.CharField(
        max_length=100,
        choices=BoolYesOrNoSelect,
        default="No",
        db_index=True,
        verbose_name="是否开启2fa",
    )
    adjust_victor = models.PositiveIntegerField(
        default=0,
        verbose_name="调解胜利"
    )
    adjust_fail = models.PositiveIntegerField(
        default=0,
        verbose_name="调解失败"
    )
    active_time = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="活跃时间",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.user_name

    def as_dict(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
        }


class UserWallet(BaseModel):
    user = models.ForeignKey(
        AuthUser,
        related_name="user_wallet_rel",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="用户",
    )
    asset = models.ForeignKey(
        Asset,
        related_name="user_wallet_asset",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="资产",
    )
    chain_name = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="链名称",
    )
    pubkey = models.CharField(
        max_length=512,
        default="",
        blank=True,
        null=True,
        verbose_name="公钥",
    )
    privkey = models.CharField(
        max_length=512,
        default="",
        blank=True,
        null=True,
        verbose_name="私钥",
    )
    address = models.CharField(
        max_length=128,
        default="",
        blank=True,
        null=True,
        verbose_name="地址",
    )
    balance = DecField(
        default=d0,
        verbose_name="钱包余额"
    )
    in_amount = DecField(
        default=d0,
        verbose_name="钱包入账"
    )
    out_amount = DecField(
        default=d0,
        verbose_name="钱包出账"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "用户钱包表"
        verbose_name_plural = "用户钱包表"

    def __str__(self):
        return self.address

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
        }


class WalletRecord(BaseModel):
    user = models.ForeignKey(
        AuthUser,
        related_name="wallet_record_user",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="用户",
    )
    asset = models.ForeignKey(
        Asset,
        related_name="wallet_record_asset",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="资产",
    )
    chain_name = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="链名称",
    )
    from_addr = models.CharField(
        max_length=128,
        default="",
        blank=True,
        null=True,
        verbose_name="转出地址",
    )
    to_addr = models.CharField(
        max_length=128,
        default="",
        blank=True,
        null=True,
        verbose_name="转入地址",
    )
    amount = DecField(
        default=d0,
        verbose_name="转账金额"
    )
    tx_fee = DecField(
        default=d0,
        verbose_name="转账手续费"
    )
    tx_hash = models.CharField(
        max_length=128,
        default="",
        blank=True,
        null=True,
        verbose_name="交易Hash",
    )
    comment = models.CharField(
        max_length=128,
        default="",
        blank=True,
        null=True,
        verbose_name="备注",
    )
    w_or_d = models.CharField(
        max_length=100,
        choices=WithdrawDeposit,
        default="Withdraw",
        verbose_name="充值提现",
    )
    status = models.CharField(
        max_length=100,
        choices=WalletStatus,
        default="Checked",
        verbose_name="状态",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "钱包充值提现记录表"
        verbose_name_plural = "钱包充值提现记录表"

    def __str__(self):
        return ""

    def as_dict(self):
        return {"id": self.id}


class TansRecord(BaseModel):
    user = models.ForeignKey(
        AuthUser,
        related_name="trans_relate_record_user",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="用户",
    )
    asset = models.ForeignKey(
        Asset,
        related_name="trans_relate_record_asset",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="资产",
    )
    amount = DecField(
        default=d0,
        verbose_name="金额"
    )
    trans_way = models.CharField(
        max_length=100,
        choices=TransWay,
        default="Input",
        verbose_name="收入支出",
    )
    source = models.CharField(
        max_length=1280,
        default="",
        blank=True,
        null=True,
        verbose_name="支付收入来源",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "钱包交易记录表"
        verbose_name_plural = "钱包交易记录表"

    def __str__(self):
        return ""

    def as_dict(self):
        return {"id": self.id}


class UserAddress(BaseModel):
    user = models.ForeignKey(
        AuthUser,
        related_name="user_address_rel",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="用户",
    )
    user_name = models.CharField(
        max_length=100,
        default="columbos",
        blank=True,
        null=True,
        verbose_name="用户名",
    )
    phone = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="手机号码",
    )
    address = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="地址",
    )
    is_set = models.CharField(
        max_length=100,
        choices=BoolYesOrNoSelect,
        default="No",
        verbose_name="是不是默认地址",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "用户收货地址表"
        verbose_name_plural = "用户收货地址表"

    def __str__(self):
        return ""

    def as_dict(self):
        return {"id": self.id}


class UserDataStat(BaseModel):
    user = models.ForeignKey(
        AuthUser,
        related_name="user_data_stat_rel",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="用户",
    )
    asset = models.ForeignKey(
        Asset,
        related_name="user_stat_asset",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="资产",
    )
    order_nums = DecField(
        default=d0,
        verbose_name="订单数量"
    )
    order_amount = DecField(
        default=d0,
        verbose_name="订单总计金额"
    )
    in_amount = DecField(
        default=d0,
        verbose_name="收入总计"
    )
    out_amount = DecField(
        default=d0,
        verbose_name="支出总计"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "用户数据统计表"
        verbose_name_plural = "用户数据统计表"

    def as_dict(self):
        return {"id": self.id}

