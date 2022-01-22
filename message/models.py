# encoding=utf-8

from django.db import models

from clbauth.models import AuthUser
from common.helpers import d0
from common.models import BaseModel, BoolYesOrNoSelect, AdminOrUser


MsgType = [
    (x, x) for x in ["Img", "Word"]
]


HelpDeskProcess = [
    (x, x) for x in ["UnHandle", "Handling", "Handled"]
]


class HelpDesk(BaseModel):
    user = models.ForeignKey(
        AuthUser,
        related_name="hd_submit_user",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="提交工单的用户",
    )
    title = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="反馈标题",
    )
    content = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="反馈内容",
    )
    top_hd_id = models.PositiveIntegerField(
        default=0,
        verbose_name="主题工单"
    )
    process = models.CharField(
        max_length=100,
        choices=HelpDeskProcess,
        default="UnHandle",
        db_index=True,
        blank=True,
        null=True,
        verbose_name="是否处理",
    )
    admin_user = models.CharField(
        max_length=100,
        choices=AdminOrUser,
        default="User",
        db_index=True,
        blank=True,
        null=True,
        verbose_name="是否处理",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "反馈表"
        verbose_name_plural = "反馈表"

    def __str__(self):
        return self.title

    def as_dict(self):
        return {"id": self.id}


class MsgFriends(BaseModel):
    user = models.ForeignKey(
        AuthUser,
        related_name="msg_friends_user",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="发送消息的用户",
    )
    friends = models.ForeignKey(
        AuthUser,
        related_name="my_friends_user",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="发送消息的用户",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "好友表"
        verbose_name_plural = "好友表"

    def __str__(self):
        return ""

    def as_dict(self):
        return {"id": self.id}


class Message(BaseModel):
    send_user = models.ForeignKey(
        AuthUser,
        related_name="message_send_user",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="发送消息的用户",
    )
    recv_user = models.ForeignKey(
        AuthUser,
        related_name="message_recv_user",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="接收消息用户",
    )
    msg_type = models.CharField(
        max_length=100,
        choices=MsgType,
        default="Word",
        blank=True,
        null=True,
        verbose_name="消息内容",
    )
    msg_content = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="消息内容",
    )
    msg_img = models.ImageField(
        upload_to="msg_img/%Y/%m/%d/",
        verbose_name="聊天图片",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "消息表"
        verbose_name_plural = "消息表"

    def __str__(self):
        return ""

    def as_dict(self):
        return {"id": self.id}
