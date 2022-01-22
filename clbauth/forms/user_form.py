# encoding=utf-8

import logging
import re
from captcha.fields import CaptchaField
from django import forms
from clbauth.models import AuthUser
from django.core.files.base import ContentFile


class AuthUserRegisterForm(forms.Form):
    user_name = forms.CharField(
        required=True,
        label="用户名",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入用户名", "class": "el-input"}
        ),
        error_messages={"required": "请输入用户名, 用户名不能为空"},
    )
    password = forms.CharField(
        required=True,
        label="密码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "password", "placeholder": "请输入密码, 数字字母均可以长度大于8位小于20位", "class": "el-input"}
        ),
        error_messages={"required": "请输入密码, 密码不能为空"},
    )
    c_password = forms.CharField(
        required=True,
        label="密码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "password", "placeholder": "请输入确认密码", "class": "el-input"}
        ),
        error_messages={"required": "请输入确认密码, 确认密码不能为空"},
    )
    pin_code = forms.CharField(
        required=True,
        label="Pin码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "password", "placeholder": "请输入Pin码(数字字母均可以长度大于6位)", "class": "el-input"}
        ),
        error_messages={"required": "请输入Pin码, Pin码不能为空"},
    )
    captcha = CaptchaField(error_messages={"invalid": "验证码错误, 请核对后在输入"})

    def __init__(self, request, *args, **kw):
        self.request = request
        super(AuthUserRegisterForm, self).__init__(*args, **kw)

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        if user_name in ["", None]:
            raise forms.ValidationError('用户名字不能为空')
        user_exist = AuthUser.objects.filter(user_name=user_name).first()
        if user_exist is not None:
            raise forms.ValidationError('该用户名已经注册, 请重新选择用户名')
        return user_name

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password in ["", None]:
            raise forms.ValidationError('密码不能为空')
        if not re.match('''[-`=\\\[\];',./~!@#$%^&*()_+|{}:"<>?A-Za-z0-9]{8,}$''', password):
            raise forms.ValidationError('密码设置不符合要求，需要大于8位, 可以是数字，字母和字符的组合')
        return password

    def clean_c_password(self):
        password = self.clean_password()
        c_password = self.cleaned_data.get('c_password')
        if c_password in ["", None]:
            raise forms.ValidationError('确认密码不能为空')
        if password != c_password:
            raise forms.ValidationError('两次输入的密码不一样')
        return c_password

    def clean_pin_code(self):
        pin_code = self.cleaned_data.get('pin_code')
        if pin_code in ["", None]:
            raise forms.ValidationError('Pin 码不能为空')
        if len(pin_code) < 6:
            raise forms.ValidationError('Pin 的长度需要大于 6 位')
        return pin_code

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        return captcha

    def save_register_user(self):
        create_user = AuthUser.objects.create(
            user_name=self.clean_user_name(),
            password=self.clean_password(),
            pin_code=self.clean_pin_code()
        )
        return create_user


class BeforLoginForm(forms.Form):
    user_name = forms.CharField(
        required=True,
        label="用户名",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入用户名", "class": "el-input"}
        ),
        error_messages={"required": "请输入用户名, 用户名不能为空"},
    )

    class Meta:
        model = AuthUser
        fields = [
            'user_name'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(BeforLoginForm, self).__init__(*args, **kw)

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        if user_name in ["", None]:
            raise forms.ValidationError('用户名字不能为空')
        user = self.get_user(user_name)
        if user is None:
            raise forms.ValidationError('该用户还没有注册')
        return user_name

    def get_user(self, user_name):
        return AuthUser.objects.filter(user_name=user_name).first()


class AuthUserLoginForm(forms.Form):
    password = forms.CharField(
        required=True,
        label="密码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "password", "placeholder": "请输入密码", "class": "el-input"}
        ),
        error_messages={"required": "请输入密码, 密码不能为空"},
    )
    factor = forms.CharField(
        required=False,
        label="2fa码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "password", "placeholder": "请输入双重认证", "class": "el-input"}
        ),
    )
    login_time = forms.CharField(
        initial=4,
        required=False,
        label="登陆时长",
        max_length=64,
        widget=forms.Select(
            choices=(
                ("20分钟", "20分钟"),
                ("1小时", "1小时"),
                ("6小时", "6小时"),
                ("24小时", "24小时"),
            )
        ),
    )
    captcha = CaptchaField(error_messages={"invalid": "验证码错误, 请核对后在输入"})
    user: AuthUser

    def __init__(self, user:AuthUser, request,  *args, **kw):
        self.user = user
        self.request = request
        super(AuthUserLoginForm, self).__init__(*args, **kw)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password in ["", None]:
            raise forms.ValidationError('密码不能为空')
        if self.user.password != password:
            raise forms.ValidationError('密码错误，请核对之后输入')
        return password

    def clean_factor(self):
        factor = self.cleaned_data.get('factor')
        if self.user.is_open == "Yes":
            if factor in ["", None]:
                raise forms.ValidationError('双重认证码不能为空')
            if self.user.factor != factor:
                raise forms.ValidationError('双重认证码输入错误')
        return factor

    def clean_login_time(self):
        login_time = self.cleaned_data.get('login_time')
        return login_time

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        return captcha


class UpdateUifForm(forms.ModelForm):
    user_name = forms.CharField(
        required=False,
        label="用户名",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入用户名", "class": "el-input"}
        ),
        error_messages={"required": "请输入用户名, 用户名不能为空"},
    )
    user: AuthUser

    class Meta:
        model = AuthUser
        fields = [
            'user_name'
        ]

    def __init__(self, request, user: AuthUser, *args, **kw):
        self.request = request
        self.user = user
        super(UpdateUifForm, self).__init__(*args, **kw)

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        user = AuthUser.objects.filter(user_name=user_name).first()
        if user is not None and user_name != user.user_name:
            raise forms.ValidationError('该用户名在系统中已经存在, 请选择其他的用户名')
        return user_name

    def save_user_info(self):
        self.user.user_name = self.clean_user_name()
        self.user.save()


class UpdateUserPhotoForm(forms.ModelForm):
    user_pho = forms.ImageField(required=True)
    user: AuthUser

    class Meta:
        model = AuthUser
        fields = [
            'user_pho'
        ]

    def __init__(self, request, user: AuthUser, *args, **kw):
        self.request = request
        self.user = user
        super(UpdateUserPhotoForm, self).__init__(*args, **kw)

    def clean_user_pho(self):
        user_pho = self.cleaned_data.get('user_pho')
        return user_pho

    def save_user_photo(self):
        try:
            file_content = ContentFile(self.request.FILES['user_pho'].read())
            self.user.user_pho.save(self.request.FILES['user_pho'].name, file_content)
        except:
            pass


class UpdatePasswordForm(forms.ModelForm):
    old_password = forms.CharField(
        required=True,
        label="原密码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type":"password", "placeholder": "请输入原密码", "class": "el-input"}
        ),
        error_messages={"required": "请输入原密码, 原密码不能为空"},
    )
    new_password = forms.CharField(
        required=True,
        label="新密码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type":"password", "placeholder": "请输入新密码", "class": "el-input"}
        ),
        error_messages={"required": "请输入新密码, 新密码不能为空"},
    )
    cnew_password = forms.CharField(
        required=True,
        label="确认密码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type":"password", "placeholder": "请输入确认密码", "class": "el-input"}
        ),
        error_messages={"required": "请输确认密码, 确认密码不能为空"},
    )
    user: AuthUser

    class Meta:
        model = AuthUser
        fields = [
            'old_password', 'new_password', 'cnew_password'
        ]

    def __init__(self, request, user: AuthUser, *args, **kw):
        self.request = request
        self.user = user
        super(UpdatePasswordForm, self).__init__(*args, **kw)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if old_password != self.user.password:
            raise forms.ValidationError('您输入的原密码不正确')
        return old_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if not re.match('''[-`=\\\[\];',./~!@#$%^&*()_+|{}:"<>?A-Za-z0-9]{8,}$''', new_password):
            raise forms.ValidationError('密码设置不符合要求，需要大于8位, 可以是数字，字母和字符的组合')
        return new_password

    def clean_cnew_password(self):
        new_password = self.cleaned_data.get('new_password')
        cnew_password = self.cleaned_data.get('cnew_password')
        if new_password != cnew_password:
            raise forms.ValidationError('您输入的确认密码和密码不一样')
        return cnew_password

    def update_password(self):
        self.user.password = self.clean_new_password()
        self.user.save()


class UpdatePincodeForm(forms.ModelForm):
    old_pincode = forms.CharField(
        required=True,
        label="原Pin码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type":"password", "placeholder": "请输入原Pin码", "class": "el-input"}
        ),
        error_messages={"required": "请输入原Pin码, 原密码不能为空"},
    )
    new_pincode = forms.CharField(
        required=True,
        label="新密Pin码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "password", "placeholder": "请输入新Pin码", "class": "el-input"}
        ),
        error_messages={"required": "请输入新Pin码, 新Pin码不能为空"},
    )
    cnew_pincode = forms.CharField(
        required=True,
        label="确认 Pin 码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type":"password", "placeholder": "请输入确认 Pin 码", "class": "el-input"}
        ),
        error_messages={"required": "请输确认 Pin 码, 确认 Pin 码不能为空"},
    )
    user: AuthUser

    class Meta:
        model = AuthUser
        fields = [
            'old_pincode', 'new_pincode', 'cnew_pincode'
        ]

    def __init__(self, request, user: AuthUser, *args, **kw):
        self.request = request
        self.user = user
        super(UpdatePincodeForm, self).__init__(*args, **kw)

    def clean_old_pincode(self):
        old_pincode = self.cleaned_data.get('old_pincode')
        if old_pincode != self.user.pin_code:
            raise forms.ValidationError('您输入的原PIN码不正确')
        return old_pincode

    def clean_new_pincode(self):
        new_pincode = self.cleaned_data.get('new_pincode')
        if not re.match('''[-`=\\\[\];',./~!@#$%^&*()_+|{}:"<>?A-Za-z0-9]{6,}$''', new_pincode):
            raise forms.ValidationError('Pin码设置不符合要求，需要大于6位, 可以是数字，字母和字符的组合')
        return new_pincode

    def clean_cnew_pincode(self):
        new_pincode = self.cleaned_data.get('new_pincode')
        cnew_pincode = self.cleaned_data.get('cnew_pincode')
        if new_pincode != cnew_pincode:
            raise forms.ValidationError('您输入的确认PIN码和PIN码不一样')
        return cnew_pincode

    def update_pincode(self):
        self.user.pin_code = self.clean_new_pincode()
        self.user.save()


class UpdateGpgForm(forms.ModelForm):
    user_public_key = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'style': 'height:200px; width:800px;outline: none;padding: 15px;box-sizing: border-box;'})
    )
    is_open = forms.CharField(
        initial=2,
        required=True,
        label="是否开启",
        max_length=64,
        widget=forms.Select(
            choices=(
                ("Yes", "开启"),
                ("No",  "关闭"),
            )
        ),
    )
    user: AuthUser

    class Meta:
        model = AuthUser
        fields = [
            'user_public_key', 'is_open'
        ]

    def __init__(self, request, user: AuthUser, *args, **kw):
        self.request = request
        self.user = user
        super(UpdateGpgForm, self).__init__(*args, **kw)

    def clean_user_public_key(self):
        user_public_key = str(self.cleaned_data.get('user_public_key'))
        return user_public_key

    def clean_is_open(self):
        is_open = self.cleaned_data.get('is_open')
        return is_open

    def update_pgp(self):
        self.user.user_public_key = self.clean_user_public_key()
        self.user.is_open = self.clean_is_open()
        self.user.save()


class ForgetPasswordForm(forms.ModelForm):
    user_name = forms.CharField(
        required=True,
        label="用户名",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "text", "placeholder": "请输入用户名", "class": "el-input"}
        ),
        error_messages={"required": "请输入用户名, 用户名不能为空"},
    )
    pincode = forms.CharField(
        required=True,
        label="Pin码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "password", "placeholder": "请输入Pin码", "class": "el-input"}
        ),
        error_messages={"required": "请输入Pin码, Pin码不能为空"},
    )

    new_password = forms.CharField(
        required=True,
        label="新密码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "password", "placeholder": "请输入新密码", "class": "el-input"}
        ),
        error_messages={"required": "请输入新密码, 新密码不能为空"},
    )

    cnew_password = forms.CharField(
        required=True,
        label="确认密码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "password", "placeholder": "请输入确认密码", "class": "el-input"}
        ),
        error_messages={"required": "请输确认密码, 确认密码不能为空"},
    )

    class Meta:
        model = AuthUser
        fields = [
            'user_name', 'pincode', 'new_password', 'cnew_password'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(ForgetPasswordForm, self).__init__(*args, **kw)

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        if user_name in ["", None]:
            raise forms.ValidationError('您输入的用户名为空')
        return user_name

    def clean_pincode(self):
        user_name = self.cleaned_data.get('user_name')
        if user_name in ["", None]:
            raise forms.ValidationError('您输入的用户名为空')
        user = AuthUser.objects.filter(user_name=user_name).first()
        pincode = self.cleaned_data.get('pincode')
        if pincode != user.pin_code:
            raise forms.ValidationError('您输入的Pin码不正确')
        return pincode

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if not re.match('''[-`=\\\[\];',./~!@#$%^&*()_+|{}:"<>?A-Za-z0-9]{8,}$''', new_password):
            raise forms.ValidationError('密码设置不符合要求，需要大于8位, 可以是数字，字母和字符的组合')
        return new_password

    def clean_cnew_password(self):
        new_password = self.cleaned_data.get('new_password')
        cnew_password = self.cleaned_data.get('cnew_password')
        if new_password != cnew_password:
            raise forms.ValidationError('您输入的确认密码和密码不一样')
        return cnew_password

    def update_password(self):
        user = AuthUser.objects.filter(user_name=self.clean_user_name()).first()
        user.password = self.clean_new_password()
        user.save()
