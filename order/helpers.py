import logging
import uuid
from decimal import Decimal
from django.utils import timezone
from clbauth.models import AuthUser, UserAddress
from common.models import Asset
from goods.models import Goods, GoodsOrder, OrderStatus
from common.helpers import d0, dec
from marchant.models import MarchantOrderFlow


# 创建订单
def create_goods_order(goods: Goods, goods_quantity: int, pay_asset_name:str, pay_coin_amount: dec, auth_user: AuthUser, user_addr: UserAddress) -> GoodsOrder:
    asset = Asset.objects.get(name=pay_asset_name)
    goods_order = GoodsOrder.objects.create(
        goods=goods,
        merchant=goods.merchant,
        goods_name=goods.name,
        goods_detail=goods.detail,
        logo=goods.logo,
        user=auth_user,
        buy_nums=goods_quantity,
        pay_way=goods.pay_way,
        pay_coin_amount=pay_coin_amount,
        order_number=uuid.uuid4().hex,
        pay_at=timezone.now(),
        is_active=True,
        status=OrderStatus.PAY_SUCCESS.value,
        user_address=user_addr,
        pay_asset=asset,
        goods_price=goods.price,
        asset_cny_price=asset.cny_price,
        cny_amount=goods.price * goods_quantity,
    )
    for attr in goods.goods_atrr.all():
        goods_order.goods_atrr.add(attr)
    goods_order.save()
    return goods_order


# 生成商家流水
def create_marchant_flow(goods: Goods, order_id: int, pay_asset_name:str, pay_coin_amount: dec) -> MarchantOrderFlow:
    asset = Asset.objects.get(name=pay_asset_name)
    marchant_flow = MarchantOrderFlow.objects.create(
        marchant=goods.merchant,
        order_id=order_id,
        asset=asset,
        coin_amount=pay_coin_amount
    )
    return marchant_flow