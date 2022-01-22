# encoding=utf-8

import logging
from django.shortcuts import redirect, render, reverse
from clbauth.models import AuthUser
from backend.forms.news_form import NewsForm
from news.models import News
from common.helpers import paged_items
from message.models import HelpDesk
from backend.helper import check_admin_login

@check_admin_login
def bnews_list(request):
    self_bar = "help"
    b_news_list = News.objects.all().order_by("-id")
    b_news_list = paged_items(request, b_news_list)
    return render(request, "backend/help_center/bnews_list.html", locals())

@check_admin_login
def bnews_detail(request, nid):
    self_bar = "help"
    bnews = News.objects.filter(id=nid).first()
    return render(request, "backend/help_center/bnews_detail.html", locals())

@check_admin_login
def create_bnews(request):
    self_bar = "help"
    if request.method == "GET":
        bnews_form = NewsForm(request)
        return render(request, "backend/help_center/create_bnews.html", locals())
    if request.method == "POST":
        bnews_form = NewsForm(request, request.POST)
        if bnews_form.is_valid():
            bnews_form.create_news()
            return redirect("bnews_list")
        else:
            error = bnews_form.errors
            return render(
                request,
                "backend/help_center/create_bnews.html",
                {
                    'bnews_form': bnews_form,
                    'error': error
                }
            )

@check_admin_login
def update_bnews(request, nid):
    self_bar = "help"
    news = News.objects.filter(id=nid).first()
    news_id = nid
    if request.method == "GET":
        bnews_form = NewsForm(request, instance=news)
        return render(request, "backend/help_center/update_bnews.html", locals())
    if request.method == "POST":
        bnews_form = NewsForm(request, request.POST, instance=news)
        if bnews_form.is_valid():
            bnews_form.update_news(nid)
            return redirect("bnews_list")
        else:
            error = bnews_form.errors
            return render(
                request,
                "backend/help_center/update_bnews.html",
                {
                    'bnews_form': bnews_form,
                    'error': error
                }
            )

@check_admin_login
def delete_news(request, nid):
    News.objects.filter(id=nid).delete()
    return redirect("bnews_list")


@check_admin_login
def bhd_list(request):
    self_bar = "help"
    user_name = request.GET.get("user_name", "")
    help_dk_list = HelpDesk.objects.filter(top_hd_id=0).order_by("-id")
    if user_name not in ["", "all", None, "None"]:
        user = AuthUser.objects.filter(user_name=user_name).first()
        help_dk_list = help_dk_list.filter(user=user)
    help_dk_list = paged_items(request, help_dk_list)
    return render(request, "backend/help_center/hd_list.html", locals())


@check_admin_login
def bhd_detail(request, top_id):
    self_bar = "help"
    user_id = int(request.session.get("user_id"))
    ht_dtl = HelpDesk.objects.filter(id=top_id).first()
    hd_dtl_list = HelpDesk.objects.filter(
        user__id=user_id,
        top_hd_id=top_id
    ).order_by("-id")
    topic_id = top_id
    return render(request, "backend/help_center/hd_detail.html", locals())


@check_admin_login
def bhd_reply(request):
    topic_id = int(request.POST.get("topic_id", 0))
    content = request.POST.get("content", "")
    user_id = int(request.session.get("user_id"))
    auth_user = AuthUser.objects.filter(id=user_id).first()
    if content not in ["", None]:
        HelpDesk.objects.filter(id=topic_id).update(process="Handling")
        HelpDesk.objects.create(
            user=auth_user,
            title="工单处理流程",
            content=content,
            top_hd_id=topic_id,
            process="Handled",
            admin_user="Admin"
        )
    return redirect("bhd_detail", topic_id)


def bhd_close(request, tid):
    HelpDesk.objects.filter(
        id=int(tid)
    ).update(process="Handled")
    return redirect("bhd_list")

