# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("frontend.urls")),
    path("backend/", include("backend.urls")),
    path("captcha", include("captcha.urls")),
    re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # 增加此行
]
