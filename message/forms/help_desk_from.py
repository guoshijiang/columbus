# encoding=utf-8

import logging
from django import forms
from message.models import HelpDesk
from clbauth.models import AuthUser


class HelpDeskForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        label="反馈标题",
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入反馈标题", "class": "el-input"}
        ),
        error_messages={"invalid": "请输入反馈标题, 反馈标题不能为空"},
    )
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'style': 'height:200px; width:800px'})
    )

    class Meta:
        model = HelpDesk
        fields = [
            'title', 'content'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(HelpDeskForm, self).__init__(*args, **kw)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        return content

    def save_hd_data(self, user_id: int):
        user = AuthUser.objects.filter(id=user_id).order_by("-id").first()
        create_hd = HelpDesk.objects.create(
            user=user,
            title=self.clean_title(),
            content=self.clean_content(),
        )
        return create_hd
