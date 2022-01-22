# encoding=utf-8

import pytz
from django.conf import settings
from django.db.models import F, Q
from django.shortcuts import redirect, render, reverse
from common.helpers import d0, dec, paged_items
from common.models import Asset
from frontend.views.utils.base import keep_four, keep_two
from goods.models import (
    Goods,
    GoodsCat,
    GoodsSate,
    GoodsComment,
    GoodsCollect
)
from marchant.models import Marchant
from clbauth.models import UserAddress, AuthUser
from clbauth.help import (
    check_user_login, check_web_enter
)


# 商品列表
@check_web_enter
def goods_list(request):
    goods_name = request.POST.get("goods_name", None)
    marchant_id = int(request.POST.get("marchant_id", 0))
    type_name = request.POST.get("type_name", "all")
    cat_id = int(request.POST.get("cat_id", 0))
    state_id = int(request.POST.get("state_id", 0))
    order_by = request.POST.get("order_by", "all")
    pay_way = request.POST.get("pay_way", "all")
    start_price = dec(request.POST.get("start_price", 0))
    end_price = dec(request.POST.get("end_price", 99999999.99))
    goods_list = Goods.objects.filter(is_sale="Yes", is_active=True).order_by("-id")
    if goods_name not in ["", None, "all"]:
        goods_list = goods_list.filter(name__contains=goods_name)
    if marchant_id not in [0, "0", "all"]:
        marchant = Marchant.objects.filter(id=marchant_id).first()
        if marchant is not None:
            goods_list = goods_list.filter(merchant=marchant)
    if cat_id not in [0, "0", "all"]:
        g_cat = GoodsCat.objects.filter(id=cat_id).first()
        if g_cat is not None:
            goods_list = goods_list.filter(goods_cat=g_cat)
    if state_id not in [0, "0", "all"]:
        g_state = GoodsSate.objects.filter(id=state_id).first()
        if g_state is not None:
            goods_list = goods_list.filter(origin_state=g_state)
    if order_by in ["time", "price", "sell"]:
        if order_by == "time":
            goods_list = goods_list.order_by("created_at")
        if order_by == "price":
            goods_list = goods_list.order_by("price")
        if order_by == "sell":
            goods_list = goods_list.order_by("sell_nums")
    if pay_way in ["ETH", "USDT"]:
        goods_list = goods_list.filter(pay_way=pay_way)
    if type_name not in ["", "all"]:
        goods_list = goods_list.filter(goods_type=type_name)
    if end_price not in [d0,  0, "0"]:
        goods_list = goods_list.filter(price__gte=start_price, price__lte=end_price)
    goods_list = paged_items(request, goods_list)
    return render(request, "front/goods/goods_list.html", locals())


# 商品详情
@check_web_enter
@check_user_login
def goods_detail(request, id):
    user_id = int(request.session.get("user_id"))
    tab = request.GET.get("tab", "goods")
    tip_msg = request.GET.get("tip_msg", "")
    user_addr_list = UserAddress.objects.filter(user__id=user_id).order_by("-id")
    len_addr = len(user_addr_list)
    if len_addr > 0:
        has_addr = True
    else:
        has_addr = False
    goods_detail = Goods.objects.filter(id=id).first()
    if goods_detail is not None:
        goods_detail.views += 1
        goods_detail.save()
        eth_asset = Asset.objects.filter(name="ETH").first()
        usdt_asset = Asset.objects.filter(name="USDT").first()
        goods_eth_p = keep_four(
            goods_detail.price / dec(eth_asset.cny_price)
        )
        goods_usdt_p = keep_four(
            goods_detail.price / dec(usdt_asset.cny_price)
        )
        goods_detail.price = keep_two(goods_detail.price)
        comment_list = GoodsComment.objects.filter(goods=goods_detail)
        comment_list = paged_items(request, comment_list)
    return render(request, "front/goods/goods_detail.html", locals())


@check_web_enter
@check_user_login
def goods_collect(request, gid):
    user_id = int(request.session.get("user_id"))
    auth_user = AuthUser.objects.get(id=user_id)
    goods_detail = Goods.objects.filter(id=gid).first()
    goods_clt = GoodsCollect.objects.filter(user=auth_user, goods=goods_detail).first()
    if goods_clt is None:
        GoodsCollect.objects.create(
            user=auth_user,
            goods=goods_detail,
        )
    return redirect(goods_collect_list)


@check_web_enter
@check_user_login
def goods_collect_list(request):
    side_bar = "goods_collect_list"
    user_id = int(request.session.get("user_id"))
    goods_clt_list = GoodsCollect.objects.filter(user__id=user_id).order_by("-id")
    goods_clt_list = paged_items(request, goods_clt_list)
    return render(request, "front/goods/goods_collect_list.html", locals())


@check_web_enter
@check_user_login
def del_goods_collect(request, gid):
    GoodsCollect.objects.filter(id=gid).delete()
    return redirect(goods_collect_list)