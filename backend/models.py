# encoding=utf-8

from django.db import models
from common.models import BaseModel, BoolYesOrNoSelect


# 后台用户表
class AdminUser(BaseModel):
    name = models.CharField(
        max_length=100,
        default="admin",
        verbose_name="用户名",
    )
    password = models.CharField(
        max_length=100,
        default="",
        verbose_name="密码",
    )
    token = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="token",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

