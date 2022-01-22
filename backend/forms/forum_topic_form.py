# encoding=utf-8

from django import forms
from forum.models import FormTopic, FormCat


class FormTopicForm(forms.ModelForm):
    cat = forms.ModelChoiceField(
        empty_label="请选择",
        queryset=FormCat.objects.filter(is_active=True)
    )
    name = forms.CharField(
        required=True,
        label="论坛主题名称",
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入论坛主题名称", "class": "el-input"}
        ),
        error_messages={"invalid": "请输入论坛主题名称, 论坛主题名称不能为空"},
    )
    introduce = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'style': 'height:200px; width:800px'})
    )

    class Meta:
        model = FormTopic
        fields = [
            'cat', 'name', 'introduce'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(FormTopicForm, self).__init__(*args, **kw)

    def clean_cat(self):
        cat = self.cleaned_data.get('cat')
        return cat

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name in ['', None]:
            raise forms.ValidationError('论坛主题名称不能为空')
        return name

    def clean_introduce(self):
        introduce = self.cleaned_data.get('introduce')
        if introduce in ['', None]:
            raise forms.ValidationError('论坛主题介绍不能为空')
        return introduce

    def create_ftopic(self):
        FormTopic.objects.create(
            cat=self.clean_cat(),
            name=self.clean_name(),
            introduce=self.clean_introduce(),
        )

    def update_ftopic(self, id):
        FormTopic.objects.filter(id=id).update(
            cat=self.clean_cat(),
            name=self.clean_name(),
            introduce=self.clean_introduce(),
        )
