# encoding=utf-8

import pytz
from django.conf import settings
from django.db.models import F, Q
from django.shortcuts import redirect, render, reverse
from message.models import Message, MsgFriends
from clbauth.models import AuthUser
from django.http import HttpResponseRedirect
from clbauth.help import (
    check_user_login, check_web_enter
)
from django.core.files.base import ContentFile


@check_web_enter
@check_user_login
def message_list(request):
    side_bar = "message_list"
    nav_active = 'message'
    user_id = int(request.session.get("user_id"))
    friend_id = int(request.GET.get("friend_id", 0))
    msg_friends_list = MsgFriends.objects.filter(user__id=user_id).order_by("-id")
    for mf in msg_friends_list:
        mf_msg = Message.objects.filter(
            Q(send_user__id=mf.friends.id) |
            Q(recv_user__id=mf.friends.id)
        ).order_by("-id").first()
        if mf_msg is not None:
            mf.lastest_msg = mf_msg.msg_content
        else:
            mf.lastest_msg = "暂时没有消息"
    if friend_id in [0, "0"]:
        if msg_friends_list is not None:
            msg_friends_lastest = msg_friends_list.first()
            if msg_friends_lastest is not None:
                friend_id = msg_friends_lastest.friends.id
                msg_list = Message.objects.filter(
                    Q(send_user__id=msg_friends_lastest.friends.id) |
                    Q(recv_user__id=msg_friends_lastest.friends.id)
                )
    else:
        msg_friend = MsgFriends.objects.filter(friends__id=friend_id).first()
        if msg_friend is None:
            MsgFriends.objects.create(
                user=AuthUser.objects.get(id=user_id),
                friends=AuthUser.objects.get(id=friend_id)
            )
        msg_list = Message.objects.filter(
            Q(send_user__id=friend_id) |
            Q(recv_user__id=friend_id)
        )
    return render(request, "front/message/msg_list.html", locals())


@check_web_enter
@check_user_login
def send_msg(request):
    user_id = int(request.session.get("user_id"))
    content = request.POST.get("content", None)
    file_img = request.FILES.get("file_img", None)
    send_user_id = int(request.POST.get("send_user_id"))
    recv_user_id = int(request.POST.get("recv_user_id"))
    friend_id = 0
    send_user = AuthUser.objects.filter(id=send_user_id).first()
    recv_user = AuthUser.objects.filter(id=recv_user_id).first()
    if send_user_id == user_id:
        self_mfs = MsgFriends.objects.filter(user=send_user, friends=recv_user).first()
        if self_mfs is None:
            MsgFriends.objects.create(
                user=send_user,
                friends=recv_user
            )
        frd_mfs = MsgFriends.objects.filter(user=recv_user, friends=send_user).first()
        if frd_mfs is None:
            MsgFriends.objects.create(
                user=recv_user,
                friends=send_user
            )
        friend_id = recv_user_id
    if recv_user_id == user_id:
        self_mfr = MsgFriends.objects.filter(user=recv_user, friends=send_user).first()
        if self_mfr is None:
            MsgFriends.objects.create(
                user=recv_user,
                friends=send_user,
            )
        frd_mfr = MsgFriends.objects.filter(user=send_user, friends=recv_user).first()
        if frd_mfr is None:
            MsgFriends.objects.create(
                user=send_user,
                friends=recv_user
            )
        friend_id = send_user_id
    if content not in ["", None]:
        Message.objects.create(
            send_user=AuthUser.objects.get(id=send_user_id),
            recv_user=AuthUser.objects.get(id=recv_user_id),
            msg_type="Word",
            msg_content=content,
        )
    if file_img not in ["", None]:
        create_msg = Message.objects.create(
            send_user=AuthUser.objects.get(id=send_user_id),
            recv_user=AuthUser.objects.get(id=recv_user_id),
            msg_type="Img",
        )
        file_content = ContentFile(file_img.read())
        create_msg.msg_img.save(file_img.name, file_content)
    return HttpResponseRedirect('message_list?friend_id='+str(friend_id))