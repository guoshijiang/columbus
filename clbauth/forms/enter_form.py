# encoding=utf-8

from captcha.fields import CaptchaField
from django import forms


class EnterForm(forms.Form):
    captcha = CaptchaField(error_messages={"invalid": "验证码错误, 请核对后在输入"})

    def __init__(self, request, *args, **kw):
        self.request = request
        super(EnterForm, self).__init__(*args, **kw)

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        return captcha
