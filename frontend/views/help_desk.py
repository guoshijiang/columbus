# encoding=utf-8

import pytz
from django.conf import settings
from django.db.models import F, Q
from django.shortcuts import redirect, render, reverse
from common.helpers import paged_items
from message.forms.help_desk_from import HelpDeskForm
from message.models import HelpDesk
from clbauth.help import (
    check_user_login, check_web_enter
)
from clbauth.models import AuthUser


@check_web_enter
@check_user_login
def help_desk_list(request):
    nav_active = 'support'
    user_id = int(request.session.get("user_id"))
    help_desk_list = HelpDesk.objects.filter(
        user__id=user_id,
        top_hd_id=0
    ).order_by("-id")
    help_desk_list = paged_items(request, help_desk_list)
    return render(request, "front/help_desk/hd_list.html", locals())


@check_web_enter
@check_user_login
def help_desk_detail(request, top_id):
    nav_active = 'support'
    user_id = int(request.session.get("user_id"))
    ht_dtl = HelpDesk.objects.filter(id=top_id).first()
    hd_dtl_list = HelpDesk.objects.filter(
        user__id=user_id,
        top_hd_id=top_id
    ).order_by("-id")
    topic_id = top_id
    return render(request, "front/help_desk/hd_detail.html", locals())


@check_web_enter
@check_user_login
def submit_hd(request):
    nav_active = 'support'
    user_id = int(request.session.get("user_id"))
    if request.method == "GET":
        hd_form = HelpDeskForm(request)
        return render(request, "front/help_desk/create_hd.html", locals())
    if request.method == "POST":
        hd_form = HelpDeskForm(request, request.POST)
        if hd_form.is_valid():
            hd_form.save_hd_data(user_id)
            return redirect("help_desk_list")
        else:
            error = hd_form.errors
            return render(
                request,
                "front/help_desk/create_hd.html",
                {
                    'hd_form': hd_form,
                    'error': error
                }
            )


@check_web_enter
@check_user_login
def hd_reply(request):
    topic_id = int(request.POST.get("topic_id", 0))
    content = request.POST.get("content", "")
    user_id = int(request.session.get("user_id"))
    auth_user = AuthUser.objects.filter(id=user_id).first()
    if content not in ["", None]:
        HelpDesk.objects.create(
            user=auth_user,
            title="工单处理流程",
            content=content,
            top_hd_id=topic_id,
            admin_user="User"
        )
    return redirect("help_desk_detail", topic_id)

