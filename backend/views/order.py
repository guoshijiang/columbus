# encoding=utf-8
import logging

import pytz
import time
from django.db import transaction
from django.conf import settings
from django.db.models import F, Q
from django.shortcuts import redirect, render, reverse
from common.helpers import d0, dec, paged_items
from goods.models import (
    Goods, GoodsOrder, OrederReturn, GoodsComment, GoodsImage
)
from marchant.models import Marchant
from clbauth.models import AuthUser
from backend.helper import check_admin_login


@check_admin_login
def b_order_list(request):
    self_bar = "order"
    marchant_name = request.GET.get("marchant_name", "all")
    status = request.GET.get("status", "all")
    mct_list = Marchant.objects.all().order_by("-id")
    order_lists = GoodsOrder.objects.all().order_by("-id")
    if marchant_name not in ["", None, "None", "all"]:
        marchant = mct_list.filter(name=marchant_name).first()
        order_lists = order_lists.filter(merchant=marchant)
    if status not in ["", None, "None", "all"]:
        order_lists = order_lists.filter(status=status)
    order_lists = paged_items(request, order_lists)
    return render(request, "backend/order/order_list.html", locals())

@check_admin_login
def b_order_detail(request, oid):
    self_bar = "order"
    order_dtl = GoodsOrder.objects.filter(id=oid).first()
    goods = order_dtl.goods
    order_ret = OrederReturn.objects.filter(order=order_dtl).first()
    return render(request, "backend/order/order_detail.html", locals())

@check_admin_login
def order_adjust(request, oid):
    order_dtl = GoodsOrder.objects.filter(id=oid).first()
    select_data = [
        {
            "mark": "marchant",
            "name": "出售商家"
        },{
            "mark": "user",
            "name": "购买用户"
        }
    ]
    if request.method == "GET":
        return render(request, "backend/order/order_adjust.html", locals())
    if request.method == "POST":
        vector = request.POST.get("vector")
        fail = request.POST.get("fail")
        reason = request.POST.get("reason")
        if vector == "marchant":  # 商家获胜； 用户失败
            marchant = order_dtl.merchant
            marchant.adjust_victor += 1
            marchant.save()
            user = order_dtl.user
            user.adjust_fail += 1
            user.save()
        if vector == "user":  # 用户获胜； 商家失败
            marchant = order_dtl.merchant
            marchant.adjust_fail += 1
            marchant.save()
            user = order_dtl.user
            user.adjust_victor += 1
            user.save()
        order_ret =OrederReturn.objects.filter(order=order_dtl).first()
        order_ret.adjust_reason = reason
        order_ret.save()
        return redirect("b_order_detail", oid)


