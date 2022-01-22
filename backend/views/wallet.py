# encoding=utf-8

import logging
from django.shortcuts import redirect, render, reverse
from clbauth.models import TansRecord, WalletRecord, AuthUser
from common.models import Asset
from backend.forms.coin_form import CoinForms
from common.helpers import paged_items
from backend.helper import check_admin_login

@check_admin_login
def coin_list(request):
    self_bar = "wallet"
    coins = Asset.objects.all().order_by("-id")
    return render(request, "backend/wallet/coin_list.html", locals())

@check_admin_login
def create_coin(request):
    self_bar = "wallet"
    if request.method == "GET":
        coin_form = CoinForms(request)
        return render(request, "backend/wallet/create_coin.html", locals())
    if request.method == "POST":
        coin_form = CoinForms(request, request.POST)
        if coin_form.is_valid():
            coin_form.create_coin()
            return redirect("coin_list")
        else:
            error = coin_form.errors
            return render(
                request,
                "backend/wallet/create_coin.html",
                {
                    'coin_form': coin_form,
                    'error': error
                }
            )

@check_admin_login
def update_coin(request, cid):
    self_bar = "wallet"
    coins = Asset.objects.filter(id=cid).first()
    coin_id = cid
    if request.method == "GET":
        coin_form = CoinForms(request, instance=coins)
        return render(request, "backend/wallet/update_coin.html", locals())
    if request.method == "POST":
        coin_form = CoinForms(request, request.POST, instance=coins)
        if coin_form.is_valid():
            coin_form.update_coin(cid)
            return redirect("coin_list")
        else:
            error = coin_form.errors
            return render(
                request,
                "backend/wallet/update_coin.html",
                {
                    'coin_form': coin_form,
                    'error': error
                }
            )

@check_admin_login
def delete_coin(request, cid):
    Asset.objects.filter(id=cid).delete()
    return redirect("coin_list")

@check_admin_login
def wd_list(request):
    self_bar = "wallet"
    user_name = request.GET.get("user_name", "")
    wt_list = WalletRecord.objects.all().order_by("-id")
    if user_name not in ["", "all", None, "None"]:
        user = AuthUser.objects.filter(user_name=user_name).first()
        wt_list = wt_list.filter(user=user)
    wt_list = paged_items(request, wt_list)
    return render(request, "backend/wallet/wd_list.html", locals())

@check_admin_login
def trans_list(request):
    self_bar = "wallet"
    user_name = request.GET.get("user_name", "")
    ts_list = TansRecord.objects.all().order_by("-id")
    if user_name not in ["", "all", None, "None"]:
        user = AuthUser.objects.filter(user_name=user_name).first()
        ts_list = ts_list.filter(user=user)
    ts_list = paged_items(request, ts_list)
    return render(request, "backend/wallet/trans_list.html", locals())

