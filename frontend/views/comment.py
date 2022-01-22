# encoding=utf-8

import pytz
from django.conf import settings
from django.db.models import F, Q
from django.shortcuts import redirect, render, reverse
from goods.models import GoodsOrder, GoodsComment
from goods.forms.comment_form import CommentForm
from clbauth.models import AuthUser
from clbauth.help import (
    check_user_login, check_web_enter
)

@check_user_login
@check_web_enter
def create_comment(request, oid):
    red_url = str(oid) + '/order_detail'
    user_id = int(request.session.get("user_id"))
    auth_user = AuthUser.objects.get(id=user_id)
    order = GoodsOrder.objects.filter(id=oid).order_by("-id").first()
    if request.method == "GET":
        cmt_form = CommentForm(request)
        return render(request, "front/order/comment/oadd_comment.html", locals())
    if request.method == "POST":
        cmt_form = CommentForm(request, request.POST)
        if cmt_form.is_valid():
            cmt_form.save_goods_comment(
                goods=order.goods,
                user=auth_user,
                merchant=order.merchant
            )
            order.status = 'FINISH'
            order.save()
            return redirect("goods_list")
        else:
            error = cmt_form.errors
            return render(request, 'front/order/comment/oadd_comment.html', {'cmt_form': cmt_form, 'error': error})



