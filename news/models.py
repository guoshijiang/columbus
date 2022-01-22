# encoding=utf-8

from django.db import models

from common.helpers import d0, dec
from common.models import (
    Asset,
    BaseModel,
    DecField,
)


class News(BaseModel):
    title = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="通知标题",
    )
    abstract = models.CharField(
        max_length=512,
        default="",
        blank=True,
        null=True,
        verbose_name="通知简介",
    )
    content = models.CharField(
        max_length=512,
        default="",
        blank=True,
        null=True,
        verbose_name="通知详情",
    )
    views = models.PositiveIntegerField(
        default=0,
        verbose_name="查看次数"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "通知表"
        verbose_name_plural = "通知表"

    def __str__(self):
        return self.title

    def as_dict(self):
        return {"id": self.id}
