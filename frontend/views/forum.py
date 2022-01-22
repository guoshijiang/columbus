# encoding=utf-8

import pytz
from django import forms
from django.conf import settings
from django.db.models import F, Q
from django.shortcuts import redirect, render, reverse
from common.helpers import paged_items
from forum.models import FormCat, FormTopic, Form, FormCommentReply
from clbauth.models import AuthUser
from forum.forms import ForumForm
from clbauth.help import (
    check_user_login, check_web_enter
)


@check_web_enter
@check_user_login
def forum_cat_list(request):
    nav_active = "forum"
    cat_lists = FormCat.objects.filter(is_active=True).order_by("-id")
    for cat in cat_lists:
        fm_last = Form.objects.filter(cat=cat).order_by("-id").first()
        fc_reply_last = FormCommentReply.objects.filter(forum=fm_last).order_by("-id").first()
        cat.lastest_reply = fc_reply_last
    cat_lists = paged_items(request, cat_lists)
    return render(request, "front/forum/forum_cat_list.html", locals())


@check_web_enter
@check_user_login
def forum_topic_list(request, fid):
    nav_active = "forum"
    cat_id = fid
    topic_list = FormTopic.objects.filter(cat__id=fid, is_active=True).order_by("-id")
    for topic in topic_list:
        topic_lst = topic_list.first()
        fm_last = Form.objects.filter(topic=topic_lst, is_active=True).order_by("-id").first()
        topic.lastest_reply = FormCommentReply.objects.filter(forum=fm_last, is_active=True).order_by("-id").first()
    form_list = Form.objects.filter(cat__id=fid, is_active=True).order_by("-id")
    for form in form_list:
        form_lst = form_list.first()
        form.lastest_reply = FormCommentReply.objects.filter(forum=form_lst, is_active=True).order_by("-id").first()
    form_list = paged_items(request, form_list)
    return render(request, "front/forum/forum_topic_list.html", locals())


@check_web_enter
@check_user_login
def forum_list_by_topic(request, fid):
    nav_active = "forum"
    topic_id = fid
    form_list = Form.objects.filter(topic__id=fid).order_by("-id")
    forum_topic = FormTopic.objects.filter(id=topic_id).first()
    cat_id = forum_topic.cat.id
    for form in form_list:
        form_lst = form_list.first()
        form.lastest_reply = FormCommentReply.objects.filter(forum=form_lst).order_by("-id").first()
    form_list = paged_items(request, form_list)
    return render(request, "front/forum/forum_list_by_topic.html", locals())


@check_web_enter
@check_user_login
def forum_detail(request, fid):
    nav_active = "forum"
    cwindow = request.GET.get("cwindow", "")
    rwindow = request.GET.get("rwindow", "")
    pwindow = request.GET.get("pwindow", "")
    frpid = int(request.GET.get("frpid", 0))
    form_dtl = Form.objects.filter(id=fid).order_by("-id").first()
    cat_id = form_dtl.cat.id
    topic_id = form_dtl.topic.id
    if cwindow in ["", None] or rwindow in ["", None] or pwindow in ["", None]:
        form_dtl.views += 1
        form_dtl.save()
    form_cmtrlpy_list = FormCommentReply.objects.filter(forum=form_dtl).order_by("-id")
    for form_cmtrlpy in form_cmtrlpy_list:
        form_cmtrlpy.reply = form_cmtrlpy_list.filter(father_forum_cy=form_cmtrlpy).order_by("-id")
        form_cmtrlpy.reply_lastest = form_cmtrlpy_list.filter(father_forum_cy=form_cmtrlpy).order_by("-id").first()
        form_cmtrlpy.nums = form_cmtrlpy_list.filter(father_forum_cy=form_cmtrlpy).count()
    form_cmtrlpy_list = paged_items(request, form_cmtrlpy_list)
    return render(request, "front/forum/forum_detail.html", locals())


@check_user_login
@check_web_enter
def forum_cmt_reply(request, fid):
    nav_active = "forum"
    father_cmt_id = int(request.POST.get("father_cmt_id", 0))
    content = request.POST.get("content", "")
    user_id = int(request.session.get("user_id"))
    user = AuthUser.objects.filter(id=user_id).first()
    form = Form.objects.filter(id=fid).order_by("-id").first()
    form.answers += 1
    form.save()
    if father_cmt_id not in ["0", 0]:
        father_forum_cy=FormCommentReply.objects.filter(id=father_cmt_id).first()
    else:
        father_forum_cy = None
    FormCommentReply.objects.create(
        user=user,
        forum=form,
        father_forum_cy=father_forum_cy,
        content=content,
    )
    return redirect("forum_detail", fid)


@check_user_login
@check_web_enter
def pulish_form(request):
    nav_active = "forum"
    user_id = int(request.session.get("user_id"))
    user = AuthUser.objects.filter(id=user_id).first()
    topic_list = FormTopic.objects.filter(is_active=True)
    if request.method == "GET":
        cat_id = request.GET.get("cat_id", 0)
        topic_id = request.GET.get("topic_id", 0)
        topic_list = topic_list.filter(cat__id=cat_id)
        if topic_id not in [0, "0", ""]:
            topic_list = topic_list.filter(id=topic_id)
        return render(request, "front/forum/publish_forum.html", locals())
    if request.method == "POST":
        cat_id = int(request.POST.get("cat_id"), 0)
        topic_id = int(request.POST.get("topic_id"), 0)
        cat = FormCat.objects.filter(id=cat_id).first()
        topic = topic_list.filter(id=topic_id).first()
        title = request.POST.get("title")
        content = request.POST.get("content")
        create_form = Form.objects.create(
            user=user,
            cat=cat,
            topic=topic,
            title=title,
            content=content
        )
        return redirect("forum_detail", create_form.id)
