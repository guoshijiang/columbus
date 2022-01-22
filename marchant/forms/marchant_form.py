# encoding=utf-8

import logging

from django import forms
from marchant.models import Marchant
from clbauth.models import AuthUser
from django.core.files.base import ContentFile


class MarchantOpenForm(forms.ModelForm):
    logo = forms.ImageField(
        required=False
    )
    name = forms.CharField(
        required=True,
        label="商户名",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入店铺名称", "class": "el-input"}
        ),
        error_messages={"required": "请输入店铺名称, 店铺名称不能为空"},
    )
    introduce = forms.CharField(
        required=True,
        label="店铺介绍",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入店铺介绍", "class": "el-input"}
        ),
        error_messages={"required": "请输入店介绍, 店铺介绍不能为空"},
    )
    detail = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'style': 'height:200px; width:800px;outline: none;padding: 15px;box-sizing: border-box;'}),
        error_messages = {"required": "请输入店铺详情, 店铺详情不能为空"},
    )
    user: AuthUser

    class Meta:
        model = Marchant
        fields = [
            'logo', 'name', 'introduce', "detail"
        ]

    def __init__(self, request, user: AuthUser, *args, **kw):
        self.request = request
        self.user = user
        super(MarchantOpenForm, self).__init__(*args, **kw)

    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        return logo

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name in ['', None]:
            raise forms.ValidationError('商家名字不能为空')
        return name

    def clean_introduce(self):
        introduce = self.cleaned_data.get('introduce')
        if introduce in ['', None]:
            raise forms.ValidationError('商家介绍不能为空')
        return introduce

    def clean_detail(self):
        detail = self.cleaned_data.get('detail')
        if detail in ['', None]:
            raise forms.ValidationError('商家详细介绍不能为空')
        return detail

    def clean_user(self):
        return self.user

    def update_marchant(self, marchant_id):
        marchant = Marchant.objects.filter(id=marchant_id).first()
        if self.request.FILES['logo'] not in ["", None]:
            file_content = ContentFile(self.request.FILES['logo'].read())
            marchant.logo.save(self.request.FILES['logo'].name, file_content)
        marchant.name = name=self.clean_name()
        marchant.introduce = self.clean_introduce()
        marchant.detail = self.clean_detail()
        marchant.save()

