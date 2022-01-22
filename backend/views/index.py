# encoding=utf-8

import pytz
from django.shortcuts import render
from backend.helper import check_admin_login
from clbauth.models import AuthUser, WalletRecord
from marchant.models import Marchant
from common.models import Asset
from django.db.models import Sum
from common.helpers import d0
from goods.models import (
    Goods, GoodsComment, GoodsOrder,
)


@check_admin_login
def b_index(request):
    self_bar = "index"
    # 总注册用户
    ttl_register_user = AuthUser.objects.all().count
    # 商家总数
    ttl_mct = Marchant.objects.all().count
    # ETH总充值
    ttl_dp_eth = WalletRecord.objects.values('amount').\
        annotate(total_d_amount=Sum('amount')).filter(
        asset=Asset.objects.filter(name="ETH").first(),
        w_or_d="Deposit"
    )
    ttl_d_eth = ttl_dp_eth[0]['total_d_amount'] if len(ttl_dp_eth) > 0 else d0
    ttl_wt_eth = WalletRecord.objects.values('amount'). \
        annotate(total_w_amount=Sum('amount')).filter(
        asset=Asset.objects.filter(name="ETH").first(),
        w_or_d="Withdraw"
    )
    ttl_w_eth = ttl_wt_eth[0]['total_w_amount'] if len(ttl_wt_eth) > 0 else d0

    ttl_dp_usdt = WalletRecord.objects.values('amount'). \
        annotate(total_d_amount=Sum('amount')).filter(
        asset=Asset.objects.filter(name="USDT").first(),
        w_or_d="Deposit"
    )
    ttl_d_usdt = ttl_dp_usdt[0]['total_d_amount'] if len(ttl_dp_usdt) > 0 else d0

    ttl_wt_usdt = WalletRecord.objects.values('amount'). \
        annotate(total_w_amount=Sum('amount')).filter(
        asset=Asset.objects.filter(name="USDT").first(),
        w_or_d="Withdraw"
    )
    ttl_w_usdt = ttl_wt_usdt[0]['total_w_amount'] if len(ttl_wt_usdt) > 0 else d0
    ttl_gds = Goods.objects.all().count()

    # 总评论次数
    ttl_cmt = GoodsComment.objects.all().count()
    ttl_order = GoodsOrder.objects.all().count()








    return render(request, "backend/index.html", locals())
