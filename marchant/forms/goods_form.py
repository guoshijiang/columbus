# encoding=utf-8

import logging

from django import forms
from marchant.models import Marchant
from goods.models import Goods, GoodsCat, GoodsSate
from clbauth.models import AuthUser
from django.core.files.base import ContentFile


class RealGoodsForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        label="商品标题",
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入商品标题", "class": "el-input"}
        ),
        error_messages={"invalid": "请输入商品标题, 商品标题不能为空"},
    )
    price = forms.DecimalField(
        required=True,
        error_messages={
            'required': '请输入正确数字价格形式'
        }
    )
    mark = forms.CharField(
        label="特殊说明",
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入特殊说明(选填),", "class": "el-input"}
        ),
    )
    total_amount = forms.IntegerField(
        initial=0,
        required=False,
        label="库存数量",
    )
    goods_cat = forms.ModelChoiceField(
        empty_label="请选择",
        queryset=GoodsCat.objects.filter(is_active=True)
    )
    origin_state = forms.ModelChoiceField(
        empty_label="请选择",
        queryset=GoodsSate.objects.filter(is_active=True)
    )
    detail = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'style': 'height:200px; width:800px;outline: none;padding: 15px;box-sizing: border-box;'})
    )
    return_goods_pc = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'style': 'height:200px; width:800px;outline: none;padding: 15px;box-sizing: border-box;'})
    )
    merchant: Marchant

    class Meta:
        model = Goods
        fields = [
            'title', "price", "mark", "total_amount", "goods_cat", "origin_state", "detail", "return_goods_pc", "merchant"
        ]

    def __init__(self, request, merchant, *args, **kw):
        self.merchant = merchant
        self.request = request
        super(RealGoodsForm, self).__init__(*args, **kw)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title in ['', None]:
            raise forms.ValidationError('商品标题不能为空')
        return title

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError('商品价格应该大于 0')
        return price

    def clean_mark(self):
        mark = self.cleaned_data.get('mark')
        return mark

    def clean_total_amount(self):
        total_amount = int(self.cleaned_data.get('total_amount'))
        if total_amount <= 0:
            raise forms.ValidationError('商品数量应该大于 0')
        return total_amount

    def clean_goods_cat(self):
        goods_cat = self.cleaned_data.get('goods_cat')
        return goods_cat

    def clean_origin_state(self):
        origin_state = self.cleaned_data.get('origin_state')
        return origin_state

    def clean_return_goods_pc(self):
        return_goods_pc = self.cleaned_data.get('return_goods_pc')
        if return_goods_pc in ['', None]:
            raise forms.ValidationError('退货政策不能为空')
        return return_goods_pc

    def clean_detail(self):
        detail = self.cleaned_data.get('detail')
        if detail in ['', None]:
            raise forms.ValidationError('商品描述不能为空')
        return detail

    def create_goods(self, goods_type):
        create_gds = Goods.objects.create(
            merchant=self.merchant,
            goods_cat=self.clean_goods_cat(),
            goods_type=goods_type,
            title=self.clean_title(),
            name=self.clean_title(),
            detail=self.clean_detail(),
            return_goods_pc=self.clean_return_goods_pc(),
            mark=self.clean_mark(),
            serveice=self.clean_mark(),
            origin_state=self.clean_origin_state(),
            total_amount=self.clean_total_amount(),
            left_amount=self.clean_total_amount(),
            price=self.clean_price(),
            is_active=True,
        )
        return create_gds

    def update_goods(self, goods_id):
        Goods.objects.filter(id=goods_id).update(
            merchant=self.merchant,
            goods_cat=self.clean_goods_cat(),
            title=self.clean_title(),
            name=self.clean_title(),
            return_goods_pc=self.clean_return_goods_pc(),
            detail=self.clean_detail(),
            mark=self.clean_mark(),
            serveice=self.clean_mark(),
            origin_state=self.clean_origin_state(),
            total_amount=self.clean_total_amount(),
            left_amount=self.clean_total_amount(),
            price=self.clean_price(),
            is_active=True,
        )
        return goods_id


class VitualGoodsForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        label="商品标题",
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入商品标题", "class": "el-input"}
        ),
        error_messages={"invalid": "请输入商品标题, 商品标题不能为空"},
    )
    price = forms.DecimalField(
        required=True,
        error_messages={
            'required': '请输入正确数字价格形式'
        }
    )
    mark = forms.CharField(
        label="特殊说明",
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入特殊说明(选填),", "class": "el-input"}
        ),
    )
    detail = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'style': 'height:200px; width:800px;outline: none;padding: 15px;box-sizing: border-box;'})
    )
    return_goods_pc = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={'style': 'height:200px; width:800px;outline: none;padding: 15px;box-sizing: border-box;'})
    )

    merchant: Marchant

    class Meta:
        model = Goods
        fields = [
            "title", "price", "mark", "return_goods_pc", "detail"
        ]

    def __init__(self, request, merchant, *args, **kw):
        self.merchant = merchant
        self.request = request
        super(VitualGoodsForm, self).__init__(*args, **kw)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title in ['', None]:
            raise forms.ValidationError('商品标题不能为空')
        return title

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError('商品价格应该大于 0')
        return price

    def clean_mark(self):
        mark = self.cleaned_data.get('mark')
        return mark

    def clean_detail(self):
        detail = self.cleaned_data.get('detail')
        if detail in ['', None]:
            raise forms.ValidationError('商品描述不能为空')
        return detail

    def clean_return_goods_pc(self):
        return_goods_pc = self.cleaned_data.get('return_goods_pc')
        if return_goods_pc in ['', None]:
            raise forms.ValidationError('退货政策不能为空')
        return return_goods_pc

    def create_goods(self, goods_type):
        create_gds = Goods.objects.create(
            merchant=self.merchant,
            goods_type=goods_type,
            title=self.clean_title(),
            name=self.clean_title(),
            mark=self.clean_mark(),
            serveice=self.clean_mark(),
            return_goods_pc=self.clean_return_goods_pc(),
            detail=self.clean_detail(),
            price=self.clean_price(),
            is_active=True,
        )
        return create_gds

    def update_goods(self, goods_id):
        Goods.objects.filter(id=goods_id).update(
            merchant=self.merchant,
            title=self.clean_title(),
            mark=self.clean_mark(),
            serveice=self.clean_mark(),
            return_goods_pc=self.clean_return_goods_pc(),
            detail=self.clean_detail(),
            price=self.clean_price(),
            is_active=True,
        )
        return goods_id




