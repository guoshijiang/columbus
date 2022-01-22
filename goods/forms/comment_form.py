# encoding=utf-8

import logging
from django import forms
from goods.models import GoodsComment


class CommentForm(forms.ModelForm):
    quality_star = forms.CharField(
        label="质量星级",
        initial=5,
        widget=forms.Select(
            choices=(('1', '1星'), ('2', '2星'), ('3', '3星'), ('4', '4星'), ('5', '5星'),)
        ),
    )
    service_star = forms.CharField(
        label="服务星级",
        initial=5,
        widget=forms.Select(
            choices=(('1', '1星'), ('2', '2星'), ('3', '3星'), ('4', '4星'), ('5', '5星'),)
        ),
    )
    trade_star = forms.CharField(
        label="交易星级",
        initial=5,
        widget=forms.Select(
            choices=(('1', '1星'), ('2', '2星'), ('3', '3星'), ('4', '4星'), ('5', '5星'),)
        ),
    )
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'style': 'height:200px; width:800px'})
    )

    class Meta:
        model = GoodsComment
        fields = [
            'quality_star', 'service_star', 'trade_star', 'content'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(CommentForm, self).__init__(*args, **kw)

    def clean_quality_star(self):
        quality_star = self.cleaned_data.get('quality_star')
        return quality_star

    def clean_service_star(self):
        service_star = self.cleaned_data.get('service_star')
        return service_star

    def clean_trade_star(self):
        trade_star = self.cleaned_data.get('trade_star')
        return trade_star

    def clean_content(self):
        content = self.cleaned_data.get('content')
        return content

    def save_goods_comment(self, goods, user, merchant):
        print(self.clean_quality_star())
        gds = GoodsComment.objects.create(
            goods=goods,
            user=user,
            merchant=merchant,
            quality_star=self.clean_quality_star(),
            service_star=self.clean_service_star(),
            trade_star=self.clean_trade_star(),
            content=self.clean_content(),
        )
        return gds