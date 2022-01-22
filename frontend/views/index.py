# encoding=utf-8

import pytz
from django.shortcuts import render

from clbauth.models import AuthUser, UserWallet
from common.models import Asset
from frontend.views.utils.base import keep_two
from frontend.views.utils.wallet import create_wallet
from goods.models import Goods, GoodsCat, GoodsSate
from marchant.models import Marchant
from news.models import News
from clbauth.help import check_web_enter, check_user_login


@check_web_enter
@check_user_login
def index(request):
    nav_active = "index"
    goods_list = Goods.objects.filter(is_sale="Yes", is_active=True)[0:20]
    for good in goods_list:
        good.price = keep_two(good.price)
    if len(goods_list) >= 2:
        goods_more = True
    else:
        goods_more = False
    marchant_list = Marchant.objects.filter(is_active=True)[0:20]
    if len(marchant_list) >= 2:
        marchant_more = True
    else:
        marchant_more = False
    news_list = News.objects.filter(is_active=True)[0:10]
    if len(news_list) >= 2:
        news_more = True
    else:
        news_more = False
    user_name = request.session.get("user_name")
    user = AuthUser.objects.filter(user_name=user_name).order_by("-id").first()
    user_btc_wallet = UserWallet.objects.filter(user=user, asset__name="BTC").first()
    user_usdt_wallet = UserWallet.objects.filter(user=user, asset__name="USDT").first()
    if user is not None:
        is_show = True
        if user.is_open == "Yes":
            open_2fa = True
            secrity = "100%"
        else:
            open_2fa = False
            secrity = "65%"
    else:
        is_show = False
    return render(request, "front/index.html", locals())
