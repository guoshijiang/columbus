# encoding=utf-8

from django import forms
from common.models import Asset
from common.helpers import d0


class CoinForms(forms.ModelForm):
    name = forms.CharField(
        required=True,
        label="币种名称",
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入币种名称", "class": "el-input"}
        ),
        error_messages={"invalid": "请输入币种名称, 币种名称不能为空"},
    )
    chain_name = forms.CharField(
        required=True,
        label="链名称",
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入链名称", "class": "el-input"}
        ),
        error_messages={"invalid": "请输入链名称, 链名称不能为空"},
    )
    unit = forms.CharField(
        required=True,
        label="币种精度",
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入币种精度", "class": "el-input"}
        ),
        error_messages={"invalid": "请输入币种精度, 币种精度不能为空"},
    )

    class Meta:
        model = Asset
        fields = [
            'name', 'chain_name', 'unit'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(CoinForms, self).__init__(*args, **kw)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name in ['', None]:
            raise forms.ValidationError('币种名称不能为空')
        return name

    def clean_chain_name(self):
        chain_name = self.cleaned_data.get('chain_name')
        if chain_name in ['', None]:
            raise forms.ValidationError('链名称不能为空')
        return chain_name

    def clean_unit(self):
        unit = self.cleaned_data.get('unit')
        if unit in ['', None]:
            raise forms.ValidationError('币种精度不能为空')
        return unit

    def create_coin(self):
        Asset.objects.create(
            name=self.clean_name(),
            chain_name=self.clean_chain_name(),
            usd_price=d0,
            cny_price=d0,
            unit=self.clean_unit(),
        )

    def update_coin(self, id):
        Asset.objects.filter(id=id).update(
            name=self.clean_name(),
            chain_name=self.clean_chain_name(),
            unit=self.clean_unit(),
        )
