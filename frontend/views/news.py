import pytz
from django.conf import settings
from django.db.models import F, Q
from django.shortcuts import redirect, render, reverse
from news.models import News
from common.helpers import paged_items
from clbauth.help import check_web_enter


@check_web_enter
def news_list(request):
    n_list = News.objects.filter(is_active=True)
    n_list = paged_items(request, n_list)
    return render(request, 'front/news/news_list.html', locals())


@check_web_enter
def news_detail(request, nid):
    news_dtl = News.objects.filter(id=nid).first()
    news_dtl.views += 1
    return render(request, 'front/news/news_detail.html', locals())