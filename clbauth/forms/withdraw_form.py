# encoding=utf-8

import logging
import re
from captcha.fields import CaptchaField
from django import forms
from clbauth.models import AuthUser, UserWallet
from common.models import Asset


class WithdrawForm(forms.Form):
    address = forms.CharField(
        required=True,
        label="地址",
        max_length=100,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入提现地址", "class": "el-input"}
        ),
        error_messages={"required": "请输入提现地址, 提现地址不能为空"},
    )
    asset = forms.ModelChoiceField(
        empty_label="请选择",
        queryset=Asset.objects.filter(is_active=True)
    )
    amount = forms.DecimalField(
        required=True,
        error_messages={
            'required': '请输入正确数字价格形式'
        }
    )
    pin_code = forms.CharField(
        required=True,
        label="Pin码",
        max_length=100,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入 Pin 码", "class": "el-input"}
        ),
        error_messages={"required": "请输入 Pin 码, Pin 码不能为空"},
    )

    factor = forms.CharField(
        required=False,
        label="2fa码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "password", "placeholder": "请输入双重认证", "class": "el-input"}
        ),
    )

    def __init__(self, request, user: AuthUser, *args, **kw):
        self.request = request
        self.user = user
        super(WithdrawForm, self).__init__(*args, **kw)

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if address in ["", None]:
            raise forms.ValidationError('地址不能为空')
        return address

    def clean_asset(self):
        asset = self.cleaned_data.get('asset')
        return asset

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError('提现金额不能小于等于 0')
        return amount

    def clean_pin_code(self):
        pin_code = self.cleaned_data.get('pin_code')
        if pin_code in ["", None]:
            raise forms.ValidationError('Pin 码不能为空')
        if pin_code != self.user.pin_code:
            raise forms.ValidationError('Pin 码不相等, 请核对后输入')
        return pin_code

    def clean_factor(self):
        factor = self.cleaned_data.get('factor')
        if self.user.is_open == "Yes":
            if factor in ["", None]:
                raise forms.ValidationError('双重认证码不能为空')
            if self.user.factor != factor:
                raise forms.ValidationError('双重认证码输入错误')
        return factor



