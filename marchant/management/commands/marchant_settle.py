# encoding=utf-8


from django.core.management.base import BaseCommand
from goods.models import GoodsOrder
from marchant.models import Marchant, MarchantOrderFlow
from clbauth.models import UserWallet, TansRecord


class Command(BaseCommand):
    def handle(self, *args, **options):
        for mct in Marchant.objects.filter(is_active=True):
            order_list = GoodsOrder.objects.filter(merchant=mct, status='FINISH', is_settle="No")
            for order in order_list:
                input_user = mct.user
                output_user = order.user
                mct_wallet = UserWallet.objects.filter(
                    user=input_user,
                    asset=order.pay_asset
                ).first()
                mct_wallet.balance += order.pay_coin_amount
                mct_wallet.in_amount += order.pay_coin_amount
                mct_wallet.save()
                TansRecord.objects.create(
                    user=input_user,
                    asset=order.pay_asset,
                    amount=order.pay_coin_amount,
                    trans_way="Input",
                    source="完成订单结算"
                )
                TansRecord.objects.create(
                    user=output_user,
                    asset=order.pay_asset,
                    amount=order.pay_coin_amount,
                    trans_way="Output",
                    source="购买商品支出"
                )
                mct_order_flow = MarchantOrderFlow.objects.filter(order_id=order.id).first()
                mct_order_flow.is_valid = "Yes"
                mct_order_flow.is_stat = "Yes"
                mct_order_flow.save()
                order.is_settle = "Yes"
                order.save()

