# encoding=utf-8

from django import forms
from news.models import News

class NewsForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        label="公告标题",
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入公告标题", "class": "el-input"}
        ),
        error_messages={"invalid": "请输入公告标题, 公告标题不能为空"},
    )
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'style': 'height:200px; width:800px'})
    )

    class Meta:
        model = News
        fields = [
            'title', 'content'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(NewsForm, self).__init__(*args, **kw)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title in ['', None]:
            raise forms.ValidationError('公告标题不能为空')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        return content

    def create_news(self):
        return News.objects.create(
            title=self.clean_title(),
            content=self.clean_content()
        )

    def update_news(self, id):
        return News.objects.filter(id=id).update(
            title=self.clean_title(),
            content=self.clean_content()
        )

