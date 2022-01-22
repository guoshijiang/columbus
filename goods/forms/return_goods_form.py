# encoding=utf-8

import logging
from django import forms
from goods.models import OrederReturn


class ReturnGoodsForm(forms.ModelForm):
    fund_ret = forms.CharField(
        label="退换货类型",
        initial=2,
        widget=forms.Select(
            choices=(('Return', '退货'), ('Exchange', '换货'),)
        ),
    )
    ret_goods_rs = forms.CharField(
        required=True,
        label="退货原因",
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入退货原因", "class": "el-input"}
        ),
        error_messages={"invalid": "请输入退货原因, 退货原因不能为空"},
    )
    qs_describe = forms.CharField(
        required=True,
        label="问题描述",
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入问题描述", "class": "el-input"}
        ),
        error_messages={"invalid": "请输入问题描述, 问题描述不能为空"},
    )
    qs_img_one = forms.ImageField(
        required=False
    )
    qs_img_two = forms.ImageField(
        required=False
    )
    qs_img_three = forms.ImageField(
        required=False
    )

    class Meta:
        model = OrederReturn
        fields = [
            'fund_ret', 'ret_goods_rs', 'qs_describe',
            "qs_img_one", "qs_img_two", "qs_img_three",
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(ReturnGoodsForm, self).__init__(*args, **kw)

    def clean_fund_ret(self):
        fund_ret = self.cleaned_data.get('fund_ret')
        return fund_ret

    def clean_ret_goods_rs(self):
        ret_goods_rs = self.cleaned_data.get('ret_goods_rs')
        return ret_goods_rs

    def clean_qs_describe(self):
        qs_describe = self.cleaned_data.get('qs_describe')
        return qs_describe

    def clean_qs_img_one(self):
        qs_img_one = self.cleaned_data.get('qs_img_one')
        return qs_img_one

    def clean_qs_img_two(self):
        qs_img_two = self.cleaned_data.get('qs_img_two')
        return qs_img_two

    def clean_qs_img_three(self):
        qs_img_three = self.cleaned_data.get('qs_img_three')
        return qs_img_three

    def save_return_data(self, order, is_send_goods):
        OrederReturn.objects.create(
            order=order,
            fund_ret=self.clean_fund_ret(),
            ret_order_status=order.status,
            ret_goods_rs=self.clean_ret_goods_rs(),
            qs_describe=self.clean_qs_describe(),
            qs_img_one=self.clean_qs_img_one(),
            qs_img_two=self.clean_qs_img_two(),
            qs_img_three=self.clean_qs_img_three(),
            is_send_goods=is_send_goods,
        )