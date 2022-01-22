# encoding=utf-8
import base64
import hashlib
import binascii
import gnupg
from django.shortcuts import redirect, render
from clbauth.forms.user_form import (
    AuthUserLoginForm,
    AuthUserRegisterForm,
    UpdateUifForm,
    UpdatePasswordForm,
    UpdatePincodeForm,
    UpdateGpgForm,
    ForgetPasswordForm,
    BeforLoginForm,
    UpdateUserPhotoForm
)
from clbauth.models import AuthUser, UserWallet
from common.models import Asset
from clbauth.help import (
    check_user_login, check_web_enter, get_code
)
from common.rsa.crypt import rsa_encrypt
from frontend.wallet_adapter import create_address, submit_withdraw
from django.http import HttpResponseRedirect


gpg = gnupg.GPG('gpg')

@check_user_login
@check_web_enter
def logout(request):
    nav_active = "index"
    if not request.session.get("is_login", None):
        return redirect("/")
    request.session.flush()
    return redirect("/")


@check_web_enter
def register(request):
    nav_active = "register"
    if request.session.get("is_login", None):
        return redirect("index")
    if request.method == "GET":
        register_form = AuthUserRegisterForm(request)
        return render(request, "front/user/register.html", locals())
    elif request.method == "POST":
        register_form = AuthUserRegisterForm(request, request.POST)
        if register_form.is_valid():
            create_auer = register_form.save_register_user()
            data_list = create_address(create_auer.id)
            print("data_list", )
            eth_address = "0x00"
            usdt_address = "0x00"
            for data in data_list:
                if data['asset_name'] == "ETH" and data['chain_name'] == "Ethereum":
                    eth_address = data['address']
                elif data['asset_name'] == "USDT" and data['chain_name'] == "Tron":
                    usdt_address = data['address']
                else:
                    continue
            asset_list = Asset.objects.filter(is_active=True)
            if asset_list is not None:
                for asset in asset_list:
                    address = "0x00"
                    if asset.name == "ETH":
                        address = eth_address
                    if asset.name == "USDT":
                        address = usdt_address
                    UserWallet.objects.create(
                        user=create_auer,
                        asset=asset,
                        chain_name=asset.chain_name,
                        address=address,
                    )
                return redirect("before_login")
            else:
                return redirect("before_login")
        else:
            error = register_form.errors
            return render(request, 'front/user/register.html', {'register_form': register_form, 'error': error})


@check_web_enter
def before_login(request):
    nav_active = "login"
    if request.session.get("is_login", None):
        return redirect("index")
    if request.method == "GET":
        before_lg_form = BeforLoginForm(request)
        return render(request, "front/user/before_login.html", locals())
    elif request.method == "POST":
        before_lg_form = BeforLoginForm(request, request.POST)
        if before_lg_form.is_valid():
            user_name = before_lg_form.clean_user_name()
            print("user_name = ", user_name)
            user = AuthUser.objects.filter(user_name=user_name).first()
            login_form = AuthUserLoginForm(user, request)
            if user is not None and user.is_open == "Yes":
                f2a_factor = get_code(6)
                try:
                    key = gpg.import_keys(user.user_public_key)
                    cipher_text_hex = gpg.encrypt(f2a_factor, key.fingerprints[0])
                except:
                    pass
                user.factor = f2a_factor
                user.save()
            return render(request, "front/user/login.html", locals())
        else:
            error = before_lg_form.errors
            return render(
                request, 'front/user/before_login.html',
                {'before_lg_form': before_lg_form, 'error': error}
            )

@check_web_enter
def login(request):
    nav_active = "login"
    user_name = request.GET.get("user_name", "")
    user = AuthUser.objects.filter(user_name=user_name).first()
    cipher_text_hex = ""
    if request.session.get("is_login", None):
        return redirect("index")
    if request.method == "GET":
        return redirect("before_login")
    elif request.method == "POST":
        login_form = AuthUserLoginForm(user, request, request.POST)
        if login_form.is_valid():
            login_time = request.POST.get("login_time", "")
            if login_time == "20分钟":
                request.session.set_expiry(20 * 60)
            if login_time == "1小时":
                request.session.set_expiry(60 * 60)
            if login_time == "6小时":
                request.session.set_expiry(6 * 60 * 60)
            if login_time == "24小时":
                request.session.set_expiry(24 * 60 * 60)
            user_eth_wallet = UserWallet.objects.filter(
                user=user, asset=Asset.objects.filter(name="ETH").first()
            ).first()
            user_usdt_wallet = UserWallet.objects.filter(
                user=user, asset=Asset.objects.filter(name="USDT").first()
            ).first()
            request.session["is_login"] = True
            request.session["user_id"] = user.id
            request.session["user_name"] = user.user_name
            request.session["user_pho"] = user.user_pho
            request.session["eth_balance"] = user_eth_wallet.balance
            request.session["eth_in_amount"] = user_eth_wallet.in_amount
            request.session["eth_out_amount"] = user_eth_wallet.out_amount
            request.session["usdt_balance"] = user_usdt_wallet.balance
            request.session["usdt_in_amount"] = user_usdt_wallet.in_amount
            request.session["usdt_out_amount"] = user_usdt_wallet.out_amount
            request.session["is_merchant"] = user.is_merchant
            request.session["member_level"] = user.member_level
            request.session["is_open"] = user.is_open
            request.session["adjust_victor"] = user.adjust_victor
            request.session["adjust_fail"] = user.adjust_fail
            request.session["join_time"] = user.created_at
            return redirect("index")
        else:
            if user is not None and user.is_open == "Yes":
                f2a_factor = get_code(6)
                try:
                    key = gpg.import_keys(user.user_public_key)
                    cipher_text_hex = gpg.encrypt(f2a_factor, key.fingerprints[0])
                except:
                    pass
                user.factor = f2a_factor
                user.save()
            error = login_form.errors
            return render(
                request, 'front/user/login.html',{
                    'login_form': login_form,
                    'error': error,
                    'user_name': user_name,
                    'cipher_text_hex': cipher_text_hex
                }
            )


@check_user_login
@check_web_enter
def account_uinfo(request):
    nav_active = 'account'
    user_id = int(request.session.get("user_id", 0))
    account_tab = "account_uinfo"
    user = AuthUser.objects.filter(id=user_id).order_by("-id").first()
    if request.method == "GET":
        uinfo_form = UpdateUifForm(request, user, instance=user)
        return render(request, "front/account/update_user_info.html", locals())
    elif request.method == "POST":
        uinfo_form = UpdateUifForm(request, user, request.POST, request.FILES)
        if uinfo_form.is_valid():
            uinfo_form.save_user_info()
            return redirect("account_uinfo")
        else:
            error = uinfo_form.errors
            return render(
                request, "front/account/update_user_info.html",
                {'user': user, 'uinfo_form': uinfo_form, 'error': error}
            )


@check_user_login
@check_web_enter
def update_password(request):
    account_tab = "update_password"
    nav_active = 'account'
    user_id = int(request.session.get("user_id", 0))
    tip_msg = request.GET.get("tip_msg", "")
    user = AuthUser.objects.filter(id=user_id).order_by("-id").first()
    if request.method == "GET":
        upd_pwd_form = UpdatePasswordForm(request, user)
        return render(request, "front/account/update_password.html", locals())
    if request.method == "POST":
        upd_pwd_form = UpdatePasswordForm(request, user, request.POST, instance=user)
        if upd_pwd_form.is_valid():
            upd_pwd_form.update_password()
            tip_msg = "修改密码成功, 请记住您的新密码"
            return HttpResponseRedirect('/update_password?tip_msg=' + tip_msg)
        else:
            error = upd_pwd_form.errors
            return render(
                request, "front/account/update_password.html",
                {'user': user, 'upd_pwd_form': upd_pwd_form, 'error': error}
            )


@check_user_login
@check_web_enter
def update_pincode(request):
    account_tab = "update_pincode"
    nav_active = 'account'
    tip_msg = request.GET.get("tip_msg", "")
    user_id = int(request.session.get("user_id", 0))
    user = AuthUser.objects.filter(id=user_id).order_by("-id").first()
    if request.method == "GET":
        upd_pform = UpdatePincodeForm(request, user)
        return render(request, "front/account/update_pin.html", locals())
    if request.method == "POST":
        upd_pform = UpdatePincodeForm(request, user, request.POST, instance=user)
        if upd_pform.is_valid():
            upd_pform.update_pincode()
            tip_msg = "修改 Pin 码成功, 请记住您的新 Pin 码"
            return HttpResponseRedirect('/update_password?tip_msg=' + tip_msg)
        else:
            error = upd_pform.errors
            return render(
                request, "front/account/update_pin.html",
                {'user': user, 'upd_pform': upd_pform, 'error': error}
            )


@check_user_login
@check_web_enter
def update_gpg(request):
    account_tab = "update_gpg"
    nav_active = 'account'
    user_id = int(request.session.get("user_id", 0))
    user = AuthUser.objects.filter(id=user_id).order_by("-id").first()
    if request.method == "GET":
        upd_gpg_form = UpdateGpgForm(request, user, instance=user)
        return render(request, "front/account/update_pgp.html", locals())
    if request.method == "POST":
        upd_gpg_form = UpdateGpgForm(request, user, request.POST, instance=user)
        if upd_gpg_form.is_valid():
            upd_gpg_form.update_pgp()
            return redirect("update_gpg")
        else:
            error = upd_gpg_form.errors
            return render(
                request, "front/account/update_pgp.html",
                {'user': user, 'upd_gpg_form': upd_gpg_form, 'error': error}
            )


@check_web_enter
def forget_password(request):
    nav_active = 'forget_password'
    tip_msg = request.GET.get("tip_msg", "")
    if request.method == "GET":
        forget_form = ForgetPasswordForm(request)
        return render(request, "front/account/forget_password.html", locals())
    if request.method == "POST":
        forget_form = ForgetPasswordForm(request, request.POST)
        if forget_form.is_valid():
            forget_form.update_password()
            tip_msg = "找回密码成功, 请记住您的新密码"
            return HttpResponseRedirect('/forget_password?tip_msg=' + tip_msg)
        else:
            error = forget_form.errors
            return render(
                request, "front/account/forget_password.html",
                {'forget_form': forget_form, 'error': error}
            )


@check_user_login
@check_web_enter
def update_user_photo(request):
    account_tab = "update_user_photo"
    nav_active = 'account'
    user_id = int(request.session.get("user_id", 0))
    user = AuthUser.objects.filter(id=user_id).order_by("-id").first()
    if request.method == "GET":
        uphoto_form = UpdateUserPhotoForm(request, user, instance=user)
        return render(request, "front/account/update_uphoto.html", locals())
    elif request.method == "POST":
        uphoto_form = UpdateUserPhotoForm(request, user, request.POST, request.FILES)
        if uphoto_form.is_valid():
            uphoto_form.save_user_photo()
            return redirect("update_user_photo")
        else:
            error = uphoto_form.errors
            return render(
                request, "front/account/update_uphoto.html",
                {'user': user, 'uphoto_form': uphoto_form, 'error': error}
            )



