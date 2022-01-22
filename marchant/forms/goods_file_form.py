# encoding=utf-8

import logging
from django import forms
from goods.models import GoodsImage


class GoodsFileForm(forms.ModelForm):
    image = forms.ImageField(
        required=True,
        error_messages={"invalid": "请输入上传商品图片, 商品图片不能为空"},
    )

    class Meta:
        model = GoodsImage
        fields = [
            'image'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(GoodsFileForm, self).__init__(*args, **kw)

    def clean_image(self):
        image = self.cleaned_data.get('image')
        return image

    def save(self):
        super(GoodsFileForm, self).save(commit=True)

