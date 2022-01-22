# encoding=utf-8

from django import forms
from forum.models import FormCat


class FormCatForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        label="论坛分类名称",
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入论坛分类名称", "class": "el-input"}
        ),
        error_messages={"invalid": "请输入论坛分类名称, 论坛分类名称不能为空"},
    )

    introduce = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'style': 'height:200px; width:800px'})
    )

    class Meta:
        model = FormCat
        fields = [
            'name', 'introduce'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(FormCatForm, self).__init__(*args, **kw)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name in ['', None]:
            raise forms.ValidationError('论坛分类名称不能为空')
        return name

    def clean_introduce(self):
        introduce = self.cleaned_data.get('introduce')
        if introduce in ['', None]:
            raise forms.ValidationError('论坛分类介绍不能为空')
        return introduce

    def create_fcat(self):
        FormCat.objects.create(
            name=self.clean_name(),
            introduce=self.clean_introduce(),
        )

    def update_fcat(self, id):
        FormCat.objects.filter(id=id).update(
            name=self.clean_name(),
            introduce=self.clean_introduce(),
        )
