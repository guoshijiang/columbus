# encoding=utf-8


import logging
from django.shortcuts import redirect, render, reverse
from forum.models import FormCat, FormTopic, Form, FormCommentReply
from backend.forms.forum_cat_form import FormCatForm
from backend.forms.forum_topic_form import FormTopicForm
from common.helpers import paged_items
from clbauth.models import AuthUser
from backend.helper import check_admin_login


@check_admin_login
def b_forum_cat(request):
    self_bar = "forum"
    fcat_list = FormCat.objects.all().order_by("-id")
    return render(request, "backend/forum/b_forum_cat.html", locals())


@check_admin_login
def create_bforum_cat(request):
    self_bar = "forum"
    if request.method == "GET":
        fcat_form = FormCatForm(request)
        return render(request, "backend/forum/create_bforum_cat.html", locals())
    if request.method == "POST":
        fcat_form = FormCatForm(request, request.POST)
        if fcat_form.is_valid():
            fcat_form.create_fcat()
            return redirect("b_forum_cat")
        else:
            error = fcat_form.errors
            return render(
                request,
                "backend/forum/create_bforum_cat.html",
                {
                    'fcat_form': fcat_form,
                    'error': error
                }
            )

@check_admin_login
def update_bforum_cat(request, cid):
    self_bar = "forum"
    fcat = FormCat.objects.filter(id=cid).first()
    cat_id = cid
    if request.method == "GET":
        fcat_form = FormCatForm(request, instance=fcat)
        return render(request, "backend/forum/update_bforum_cat.html", locals())
    if request.method == "POST":
        fcat_form = FormCatForm(request, request.POST, instance=fcat)
        if fcat_form.is_valid():
            fcat_form.update_fcat(cid)
            return redirect("b_forum_cat")
        else:
            error = fcat_form.errors
            return render(
                request,
                "backend/forum/update_bforum_cat.html",
                {
                    'fcat_form': fcat_form,
                    'error': error
                }
            )

@check_admin_login
def delete_bforum_cat(request, cid):
    FormCat.objects.filter(id=cid).delete()
    return redirect("b_forum_cat")

@check_admin_login
def b_forum_topic(request):
    self_bar = "forum"
    ftopic_list =FormTopic.objects.all().order_by("-id")
    return render(request, "backend/forum/b_forum_topic.html", locals())

@check_admin_login
def create_bforum_topic(request):
    self_bar = "forum"
    if request.method == "GET":
        ftopic_form = FormTopicForm(request)
        return render(request, "backend/forum/create_bforum_topic.html", locals())
    if request.method == "POST":
        ftopic_form = FormTopicForm(request, request.POST)
        if ftopic_form.is_valid():
            ftopic_form.create_ftopic()
            return redirect("b_forum_topic")
        else:
            error = ftopic_form.errors
            return render(
                request,
                "backend/forum/create_bforum_topic.html",
                {
                    'ftopic_form': ftopic_form,
                    'error': error
                }
            )

@check_admin_login
def update_bforum_topic(request, tid):
    self_bar = "forum"
    ftopic = FormTopic.objects.filter(id=tid).first()
    topic_id = tid
    if request.method == "GET":
        ftopic_form = FormTopicForm(request, instance=ftopic)
        return render(request, "backend/forum/update_bforum_topic.html", locals())
    if request.method == "POST":
        ftopic_form = FormTopicForm(request, request.POST, instance=ftopic)
        if ftopic_form.is_valid():
            ftopic_form.update_ftopic(tid)
            return redirect("b_forum_cat")
        else:
            error = ftopic_form.errors
            return render(
                request,
                "backend/forum/update_bforum_topic.html",
                {
                    'ftopic_form': ftopic_form,
                    'error': error
                }
            )

@check_admin_login
def delete_bforum_topic(request, tid):
    FormTopic.objects.filter(id=tid).delete()
    return redirect("b_forum_topic")


@check_admin_login
def b_forum_list(request):
    self_bar = "forum"
    user_name = request.GET.get("user_name", "")
    forum_list = Form.objects.all().order_by("-id")
    if user_name not in ["", "all", None, "None"]:
        user = AuthUser.objects.filter(user_name=user_name).first()
        forum_list = forum_list.filter(user=user)
    forum_list = paged_items(request, forum_list)
    return render(request, "backend/forum/forum_list.html", locals())

@check_admin_login
def b_forum_detail(request, fid):
    self_bar = "forum"
    forum_dtl= Form.objects.filter(id=fid).first()
    return render(request, "backend/forum/forum_detail.html", locals())

@check_admin_login
def disable_forum(request, fid):
    ftm = Form.objects.filter(id=fid).first()
    ftm.is_active = False
    ftm.save()
    return redirect("b_forum_list")

@check_admin_login
def enable_forum(request, fid):
    ftm = Form.objects.filter(id=fid).first()
    ftm.is_active = True
    ftm.save()
    return redirect("b_forum_list")

@check_admin_login
def b_forum_comment(request, fid):
    self_bar = "forum"
    fu_cmt_list = FormCommentReply.objects.filter(id=fid).order_by("-id")
    fu_cmt_list = paged_items(request, fu_cmt_list)
    return render(request, "backend/forum/forum_comment.html", locals())


