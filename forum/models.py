# encoding=utf-8

from django.db import models
from clbauth.models import AuthUser
from common.models import BaseModel, BoolYesOrNoSelect


class FormCat(BaseModel):
    name = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="论坛分类名称",
    )
    introduce = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="论坛分类介绍",
    )
    topic_num = models.PositiveIntegerField(
        default=0,
        verbose_name="主题数量"
    )
    forum_num = models.PositiveIntegerField(
        default=0,
        verbose_name="帖子数量"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "论坛分类表"
        verbose_name_plural = "论坛分类表"

    def __str__(self):
        return self.name

    def as_dict(self):
        return {"id": self.id}


class FormTopic(BaseModel):
    cat = models.ForeignKey(
        FormCat,
        related_name="form_cat_topic",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="论坛分类",
    )
    name = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="论坛主题名称",
    )
    introduce = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="论坛主题介绍",
    )
    topic_num = models.PositiveIntegerField(
        default=1,
        verbose_name="主题数量"
    )
    forum_num = models.PositiveIntegerField(
        default=0,
        verbose_name="帖子数量"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "论坛主题表"
        verbose_name_plural = "论坛主题表"

    def __str__(self):
        return self.name

    def as_dict(self):
        return {"id": self.id}


class Form(BaseModel):
    user = models.ForeignKey(
        AuthUser,
        related_name="form_pulish_user",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="论坛发布者",
    )
    cat = models.ForeignKey(
        FormCat,
        related_name="form_cat",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="论坛类别",
    )
    topic = models.ForeignKey(
        FormTopic,
        related_name="form_topic",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="论坛主题",
    )
    title = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="论坛标题",
    )
    abstract = models.CharField(
        max_length=512,
        default="",
        blank=True,
        null=True,
        verbose_name="论坛摘要",
    )
    content = models.CharField(
        max_length=1024,
        default="",
        blank=True,
        null=True,
        verbose_name="论坛内容",
    )
    views = models.PositiveIntegerField(
        default=0,
        verbose_name="论坛查看次数"
    )
    un_likes = models.PositiveIntegerField(
        default=0,
        verbose_name="论坛踩次数"
    )
    likes = models.PositiveIntegerField(
        default=0,
        verbose_name="论坛点赞次数"
    )
    answers = models.PositiveIntegerField(
        default=0,
        verbose_name="答案个数"
    )
    is_check = models.CharField(
        max_length=100,
        choices=BoolYesOrNoSelect,
        default="No",
        verbose_name="是否审核",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "论坛表"
        verbose_name_plural = "论坛表"

    def __str__(self):
        return self.content

    def as_dict(self):
        return {"id": self.id}


class FormCommentReply(BaseModel):
    user = models.ForeignKey(
        AuthUser,
        related_name="form_comment_reply_user",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="论坛发布者",
    )
    forum = models.ForeignKey(
        Form,
        related_name="form_comment_reply",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="论坛类别",
    )
    father_forum_cy = models.ForeignKey(
        "FormCommentReply",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="父论坛",
    )
    content = models.CharField(
        max_length=1024,
        default="",
        blank=True,
        null=True,
        verbose_name="论坛内容",
    )
    views = models.PositiveIntegerField(
        default=0,
        verbose_name="论坛查看次数"
    )
    un_likes = models.PositiveIntegerField(
        default=0,
        verbose_name="论坛踩次数"
    )
    likes = models.PositiveIntegerField(
        default=0,
        verbose_name="论坛点赞次数"
    )
    answers = models.PositiveIntegerField(
        default=0,
        verbose_name="答案个数"
    )
    is_check = models.CharField(
        max_length=100,
        choices=BoolYesOrNoSelect,
        default="No",
        verbose_name="是否审核",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "论坛评论回复表"
        verbose_name_plural = "论坛评论回复表"

    def __str__(self):
        return self.content

    def as_dict(self):
        return {
            "id": self.id
        }