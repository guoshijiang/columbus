# encoding=utf-8

from django import forms
from common.models import Asset
from goods.models import GoodsCat, GoodsSate


class GdsCatForms(forms.ModelForm):
    name = forms.CharField(
        required=True,
        label="类别名称",
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入类别名称", "class": "el-input"}
        ),
        error_messages={"invalid": "请输入类别名称, 类别名称不能为空"},
    )

    class Meta:
        model = GoodsCat
        fields = [
            'name'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(GdsCatForms, self).__init__(*args, **kw)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name in ['', None]:
            raise forms.ValidationError('类别名称不能为空')
        return name

    def create_gds_cat(self):
        GoodsCat.objects.create(
            name=self.clean_name()
        )

    def update_gds_cat(self, id):
        GoodsCat.objects.filter(id=id).update(
            name=self.clean_name(),
        )


class StateForms(forms.ModelForm):
    state = forms.CharField(
        required=True,
        label="地址名",
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入地址名", "class": "el-input"}
        ),
        error_messages={"invalid": "请输入地址名, 地址名不能为空"},
    )

    class Meta:
        model = GoodsSate
        fields = [
            'state'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(StateForms, self).__init__(*args, **kw)

    def clean_state(self):
        state = self.cleaned_data.get('state')
        if state in ['', None]:
            raise forms.ValidationError('地址名称不能为空')
        return state

    def create_state(self):
        GoodsSate.objects.create(
            state=self.clean_state()
        )

    def update_state(self, id):
        GoodsSate.objects.filter(id=id).update(
            state=self.clean_state()
        )
