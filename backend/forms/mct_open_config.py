# encoding=utf-8

import logging

from django import forms
from marchant.models import MarchantConfig


class MarchantOpneForm(forms.ModelForm):
    usdt_amount = forms.DecimalField(
        required=True,
        error_messages={
            'required': '请输入正确数字价格形式'
        }
    )

    class Meta:
        model = MarchantConfig
        fields = [
            "usdt_amount"
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(MarchantOpneForm, self).__init__(*args, **kw)

    def clean_usdt_amount(self):
        usdt_amount = self.cleaned_data.get('usdt_amount')
        if usdt_amount <= 0:
            raise forms.ValidationError('配置的USDT数量应该大于0')
        return usdt_amount

    def create_config(self):
        return MarchantConfig.objects.create(
            usdt_amount=self.clean_usdt_amount()
        )

    def update_config(self, id):
        return MarchantConfig.objects.filter(id=id).update(
            usdt_amount=self.clean_usdt_amount()
        )


