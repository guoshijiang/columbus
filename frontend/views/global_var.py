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


def global_variable(request):
    goods_clist = GoodsCat.objects.filter(is_active=True)
    goods_slist = GoodsSate.objects.filter(is_active=True)
    asset_eth = Asset.objects.filter(name="ETH").first()
    if asset_eth is None:
        eth_asset_name = "ETH"
        btc_chain_name = "Ethereum"
        btc_usd_price = 0
        btc_cyn_price = 0
    else:
        eth_asset_name = asset_eth.name
        eth_chain_name = asset_eth.chain_name
        eth_usd_price = asset_eth.usd_price
        eth_cyn_price = asset_eth.cny_price
    asset_usdt = Asset.objects.filter(name="USDT").first()
    if asset_usdt is None:
        usdt_asset_name = "USDT"
        usdt_chain_name = "Trc20"
        usdt_usd_price = 0
        usdt_cyn_price = 0
    else:
        usdt_asset_name = "USDT"
        usdt_chain_name = "Trc20"
        usdt_usd_price = asset_usdt.usd_price
        usdt_cyn_price = asset_usdt.cny_price
    user_name = request.session.get("user_name", None)
    if user_name not in [None, ""]:
        user = AuthUser.objects.filter(user_name=user_name).order_by("-id").first()
        user_eth_wallet = UserWallet.objects.filter(user=user, asset__name="ETH").first()
        user_usdt_wallet = UserWallet.objects.filter(user=user, asset__name="USDT").first()
    return locals()
