from django.db import transaction
from common.helpers import dec, d0
from django.db.models import F
from clbauth.models import AuthUser, UserWallet, UserAddress
from goods.models import Goods, GoodsOrder, OrderStatus, OrederReturn
from order.helpers import create_goods_order, create_marchant_flow
from order.const import (
    PayWayError,
    GoodsNotEnough,
    GoodsSellOut,
    UserBalanceNotEnough,
    CanNotBuySelfGoods,
    PayOrderSuccess,
    GoodsNotExist,
    OrderNotExist
)


@transaction.atomic
def create(goods_id: int, goods_quantity: int, pay_asset_name: str, pay_coin_amount: dec, buyer_id: int, address_id:int) -> str:
    if pay_asset_name not in ["ETH", "USDT"]:
        return PayWayError
    goods = Goods.objects.select_for_update().filter(id=goods_id).first()
    if goods is None:
        return GoodsNotExist
    if goods.left_amount <= 0:
        return GoodsSellOut
    if goods.left_amount < goods_quantity:
        return GoodsNotEnough
    user_wallet = UserWallet.objects.select_for_update().filter(
        user__id=buyer_id, asset__name=pay_asset_name
    ).first()
    if user_wallet.balance < pay_coin_amount * goods_quantity:
        return UserBalanceNotEnough
    auth_user = AuthUser.objects.get(id=buyer_id)
    if user_wallet.user == goods.merchant.user:
        return CanNotBuySelfGoods
    # 更新钱包余额
    total_pay_coin_amount = pay_coin_amount * goods_quantity
    user_wallet_h = UserWallet.objects.filter(id=user_wallet.id).first()
    user_wallet_h.balance = user_wallet_h.balance - total_pay_coin_amount
    user_wallet_h.save()
    # 更新商品的库存数量
    Goods.objects.filter(
        id=goods.id,
        left_amount__gte=goods_quantity,
        total_amount__gte=F("sell_nums") + goods_quantity,
    ).update(
        left_amount=F("left_amount") - goods_quantity,
        sell_nums=F("sell_nums") + goods_quantity,
    )
    user_addr = UserAddress.objects.filter(id=address_id).first()
    # 生成订单表
    goods_order = create_goods_order(
        goods=goods,
        goods_quantity=goods_quantity,
        pay_asset_name=pay_asset_name,
        pay_coin_amount=total_pay_coin_amount,
        auth_user=auth_user,
        user_addr=user_addr
    )
    # 生成商家流水
    create_marchant_flow(
        goods=goods,
        order_id=goods_order.id,
        pay_asset_name=pay_asset_name,
        pay_coin_amount=total_pay_coin_amount
    )
    return PayOrderSuccess


