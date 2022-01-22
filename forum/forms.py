# encoding=utf-8

import logging

from django import forms
from marchant.models import Marchant
from forum.models import FormCat, FormTopic, Form
from clbauth.models import AuthUser


class ForumForm(forms.ModelForm):
    cat = forms.ModelChoiceField(
        required=False,
        empty_label="请选择",
        queryset=FormCat.objects.filter(is_active=True)
    )
    topic = forms.ModelChoiceField(
        required=False,
        empty_label="请选择",
        queryset=FormTopic.objects.filter(is_active=True)
    )
    title = forms.CharField(
        required=True,
        label="论坛标题",
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入论坛标题", "class": "el-input"}
        ),
        error_messages={"invalid": "请输入论坛标题, 论坛标题不能为空"},
    )
    content = forms.CharField(
        required=True,
        label="论坛描述",
        widget=forms.Textarea(attrs={'style': 'height:200px; width:800px;outline: none;padding: 15px;box-sizing: border-box;'})
    )
    cat_id: int
    topic_id: int

    class Meta:
        model = Form
        fields = [
            'cat', 'topic', 'title', "content"
        ]

    def __init__(self, request, cat_id: int, topic_id: int, *args, **kw):
        self.request = request
        self.cat_id = cat_id
        self.topic_id = topic_id
        super(ForumForm, self).__init__(*args, **kw)

    def clean_cat(self):
        if self.cat_id != 0:
            cat = FormCat.objects.filter(id=self.cat_id).first()
        else:
            cat = self.cleaned_data.get('cat')
        return cat

    def clean_topic(self):
        if self.topic_id != 0:
            topic = FormTopic.objects.filter(id=self.topic_id).first()
        else:
            topic = self.cleaned_data.get('topic')
        return topic

    def clean_title(self):
        title = self.cleaned_data.get('title')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        return content

    def save_form_data(self, user_id) -> int:
        user = AuthUser.objects.filter(id=user_id).first()
        create_form = Form.objects.create(
            user=user,
            cat=self.clean_cat(),
            topic=self.clean_topic(),
            title =self.clean_title(),
            content =self.clean_content()
        )
        return create_form.topic.id