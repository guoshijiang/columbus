# encoding=utf-8

import logging
import re
from django import forms
from clbauth.models import UserAddress, AuthUser


class UseAddressForm(forms.ModelForm):
    user_name = forms.CharField(
        required=True,
        label="用户名",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入用户名", "class": "el-input"}
        ),
        error_messages={"required": "请输入用户名, 用户名不能为空"},
    )
    phone = forms.CharField(
        required=True,
        label="电话号码",
        max_length=12,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入电话号码", "class": "el-input"}
        ),
        error_messages={"required": "请输入电话号码, 电话号码不能为空"},
    )
    address = forms.CharField(
        required=True,
        label="详细地址",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入详细地址", "class": "el-input"}
        ),
        error_messages={"required": "请输入详细地址, 详细地址不能为空"},
    )

    class Meta:
        model = UserAddress
        fields = [
            'user_name', 'phone', 'address'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(UseAddressForm, self).__init__(*args, **kw)

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        if user_name in ['', None]:
            raise forms.ValidationError('用户名字不能为空')
        return user_name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone in ['', None]:
            raise forms.ValidationError('手机号码不能为空')
        if not re.match("^(1[3|4|5|6|7|8|9][0-9]\\d{4,8})$", phone):
            raise forms.ValidationError('手机号码不符合规则')
        return phone

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if address in ['', None]:
            raise forms.ValidationError('详细地址不能为空')
        return address

    def save_addr(self, user_id: int):
        user_name = self.clean_user_name()
        phone = self.clean_phone()
        address = self.clean_address()
        user = AuthUser.objects.filter(id=user_id).first()
        UserAddress.objects.create(
            user=user,
            user_name=user_name,
            phone=phone,
            address=address,
        )

    def update_addr(self, address_id: int):
        user_name = self.clean_user_name()
        phone = self.clean_phone()
        address = self.clean_address()
        user_addr = UserAddress.objects.filter(id=address_id).first()
        if user_addr is not None:
            user_addr.user_name = user_name
            user_addr.phone = phone
            user_addr.address = address
            user_addr.save()
        else:
            raise

