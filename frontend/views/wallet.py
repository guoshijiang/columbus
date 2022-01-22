# encoding=utf-8

import pytz
import qrcode
import base64
import io
import gnupg
from django.conf import settings
from django.db.models import F, Q
from django.shortcuts import redirect, render, reverse
from common.helpers import paged_items
from clbauth.models import (
    AuthUser, WalletRecord, Asset, UserWallet, TansRecord
)
from clbauth.help import get_code
from clbauth.help import (
    check_user_login, check_web_enter
)
from common.helpers import dec, d0
from clbauth.forms.withdraw_form import WithdrawForm
from common.rsa.crypt import rsa_encrypt


gpg = gnupg.GPG('gpg')

@check_web_enter
@check_user_login
def wallet_info(request):
    nav_active = 'wallet'
    user_id = int(request.session.get("user_id"))
    user_wallet_list = UserWallet.objects.filter(user__id=user_id).order_by("-id")
    total_eth_balance = d0
    total_usdt_balance = d0
    total_eth_balance_usd = d0
    total_balance_cny = d0
    total_eth_balance_cny = d0
    total_usdt_balance_cny = d0
    total_eth_in_amount = d0
    total_eth_out_amount = d0
    total_eth_in_amount_usd = d0
    total_eth_in_amount_cny = d0
    total_eth_out_amount_usd = d0
    total_eth_out_amount_cny = d0
    total_usdt_in_amount = d0
    total_usdt_out_amount = d0
    total_usdt_in_amount_cny = d0
    total_usdt_out_amount_cny = d0
    total_out_usd = d0
    total_out_cny = d0
    total_in_usd = d0
    total_in_cny = d0
    for user_wallet in user_wallet_list:
        if user_wallet.asset.name == "ETH":
            total_eth_balance += user_wallet.balance
            total_eth_balance_usd += user_wallet.balance * user_wallet.asset.usd_price
            total_eth_balance_cny += user_wallet.balance * user_wallet.asset.cny_price
            total_eth_in_amount += user_wallet.in_amount
            total_eth_in_amount_usd += user_wallet.in_amount * user_wallet.asset.usd_price
            total_eth_in_amount_cny += user_wallet.in_amount * user_wallet.asset.cny_price
            total_eth_out_amount += user_wallet.out_amount
            total_eth_out_amount_usd += user_wallet.out_amount * user_wallet.asset.usd_price
            total_eth_out_amount_cny += user_wallet.out_amount * user_wallet.asset.cny_price
        if user_wallet.asset.name == "USDT":
            total_usdt_balance += user_wallet.balance
            total_usdt_balance_cny += user_wallet.balance * user_wallet.asset.cny_price
            total_usdt_in_amount += user_wallet.in_amount
            total_usdt_in_amount_cny += user_wallet.in_amount * user_wallet.asset.cny_price
            total_usdt_out_amount += user_wallet.out_amount
            total_usdt_out_amount_cny += user_wallet.out_amount * user_wallet.asset.cny_price
    total_balance_usd = total_eth_balance_usd + total_usdt_balance
    total_balance_cny = total_eth_balance_cny + total_usdt_balance_cny
    total_out_usd = total_eth_out_amount_usd + total_usdt_out_amount
    total_out_cny = total_eth_out_amount_cny + total_usdt_out_amount_cny
    total_in_usd = total_eth_in_amount_usd + total_usdt_in_amount
    total_in_cny = total_eth_in_amount_cny + total_usdt_in_amount_cny
    return render(request, "front/wallet/wallet_info.html", locals())


@check_web_enter
@check_user_login
def wallet_record(request):
    nav_active = 'wallet'
    side_bar = "wallet_record"
    asset_id = request.GET.get("asset_id", 0)
    w_or_d = request.GET.get("w_or_d", "all")
    status = request.GET.get("status", "all")
    user_id = int(request.session.get("user_id"))
    wallet_record_list = WalletRecord.objects.filter(user__id=user_id).order_by("-id")
    if asset_id not in ["0", 0, ""]:
        wallet_record_list = wallet_record_list.filter(asset__id=asset_id)
    if w_or_d not in ["None", None, "all", ""]:
        wallet_record_list = wallet_record_list.filter(w_or_d=w_or_d)
    if status not in ["", "all", None, "None"]:
        wallet_record_list = wallet_record_list.filter(status=status)
    wallet_record_list = paged_items(request, wallet_record_list)
    return render(request, "front/wallet/wallet_record.html", locals())


@check_web_enter
@check_user_login
def wallet_trans_record(request):
    nav_active = 'wallet'
    side_bar = "wallet_trans_record"
    user_id = int(request.session.get("user_id"))
    wallet_trans = TansRecord.objects.filter(user__id=user_id).order_by("-id")
    wallet_trans = paged_items(request, wallet_trans)
    return render(request, "front/wallet/wallet_trans.html", locals())



@check_web_enter
@check_user_login
def wallet_deposit(request):
    nav_active = 'wallet'
    side_bar = "wallet_deposit"
    user_id = int(request.session.get("user_id"))
    asset = request.GET.get("asset", "eth")
    asset_db = Asset.objects.get(name=asset)
    user_wallet = UserWallet.objects.filter(user__id=user_id, asset=asset_db).first()
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=4,
    )
    qr.add_data(user_wallet.address)
    img = qr.make(fit=True)
    out = io.BytesIO()
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(out, 'PNG')
    data_steam = u"data:image/png;base64," + base64.b64encode(out.getvalue()).decode('ascii')
    return render(request, "front/wallet/wallet_deposit.html", locals())


@check_web_enter
@check_user_login
def wallet_withdraw(request):
    nav_active = 'wallet'
    side_bar = "wallet_withdraw"
    user_id = int(request.session.get("user_id"))
    user = AuthUser.objects.filter(id=user_id).first()
    cipher_text_hex = ""
    if user is not None and user.is_open == "Yes":
        f2a_factor = get_code(6)
        try:
            key = gpg.import_keys(user.user_public_key)
            cipher_text_hex = gpg.encrypt(f2a_factor, key.fingerprints[0])
        except:
            pass
        user.factor = f2a_factor
        user.save()
    user_eth_wallet = UserWallet.objects.filter(
        user__id=user_id,
        asset=Asset.objects.get(name="eth")
    ).first()
    user_usdt_wallet = UserWallet.objects.filter(
        user__id=user_id,
        asset=Asset.objects.get(name="USDT")
    ).first()
    if request.method == "GET":
        user_wallet = None
        withdraw_form = WithdrawForm(request, user, user_wallet)
        return render(request, "front/wallet/wallet_withdraw.html", locals())
    if request.method == "POST":
        withdraw_form = WithdrawForm(request, user, request.POST)
        if withdraw_form.is_valid():
            asset_db = withdraw_form.clean_asset()
            amount = withdraw_form.clean_amount()
            user_wallet = UserWallet.objects.filter(user__id=user_id, asset=asset_db).first()
            if amount > user_wallet.balance:
                return render(
                    request, 'front/wallet/wallet_withdraw.html',
                    {
                        'withdraw_form': withdraw_form,
                        'tip_msg': "钱包余额不足",
                        'user_eth_wallet': user_eth_wallet,
                        'user_usdt_wallet': user_usdt_wallet,
                        'cipher_text_hex': cipher_text_hex
                    }
                )
            w_r = WalletRecord.objects.create(
                user=user,
                asset=asset_db,
                from_addr="unknown",
                to_addr=withdraw_form.clean_address(),
                amount=withdraw_form.clean_amount()
            )
            return redirect("wallet_record")
        else:
            error = withdraw_form.errors
            return render(
                request, 'front/wallet/wallet_withdraw.html',
                {
                    'withdraw_form': withdraw_form,
                    'error': error,
                    'user_eth_wallet': user_eth_wallet,
                    'user_usdt_wallet': user_usdt_wallet,
                    'cipher_text_hex': cipher_text_hex
                }
            )


