# encoding=utf-8

import logging
from django.shortcuts import redirect, render, reverse
from clbauth.models import AuthUser, UserAddress, UserWallet, UserDataStat
from common.helpers import paged_items
from goods.models import GoodsCollect
from marchant.models import MarchantCollect
from marchant.models import MarchantBackList
from backend.helper import check_admin_login

@check_admin_login
def user_list(request):
    self_bar = "user"
    user_lsts = AuthUser.objects.all().order_by("-id")
    user_lsts = paged_items(request, user_lsts)
    return render(request, "backend/user/user_list.html", locals())


@check_admin_login
def user_detail(request, uid):
    self_bar = "user"
    user = AuthUser.objects.filter(id=uid).first()
    return render(request, "backend/user/user_detail.html", locals())


@check_admin_login
def user_wallets(request, uid):
    self_bar = "user"
    user_id = uid
    u_wallet_list = UserWallet.objects.filter(user__id=uid)
    return render(request, "backend/user/user_wallet.html", locals())

@check_admin_login
def user_recv_address(request, uid):
    self_bar = "user"
    user_id = uid
    u_addr_list = UserAddress.objects.filter(user__id=uid)
    return render(request, "backend/user/user_address.html", locals())

@check_admin_login
def user_collect_gds(request, uid):
    self_bar = "user"
    user_id = uid
    collect_gds = GoodsCollect.objects.filter(user__id=uid)
    collect_gds = paged_items(request, collect_gds)
    return render(request, "backend/user/user_collect_goods.html", locals())


def user_collect_mct(request, uid):
    self_bar = "user"
    user_id = uid
    collet_mcts = MarchantCollect.objects.filter(user__id=uid)
    collet_mcts = paged_items(request, collet_mcts)
    return render(request, "backend/user/user_collect_mct.html", locals())


def user_backlist_mct(request, uid):
    self_bar = "user"
    user_id = uid
    collet_bk_mcts = MarchantBackList.objects.filter(user__id=uid)
    collet_bk_mcts = paged_items(request, collet_bk_mcts)
    return render(request, "backend/user/user_bk_mct.html", locals())


def disable_user(request, uid):
    user = AuthUser.objects.filter(id=uid).first()
    user.is_active = False
    user.save()
    return redirect("user_list")


def enable_user(request, uid):
    user = AuthUser.objects.filter(id=uid).first()
    user.is_active = True
    user.save()
    return redirect("user_list")