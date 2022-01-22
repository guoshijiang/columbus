import logging

from django.shortcuts import redirect, render, reverse
from clbauth.models import AuthUser, UserAddress, UserWallet
from common.models import Asset
from goods.models import (
    Goods, GoodsOrder, OrederReturn, OrderStatus
)
from order.controller import create
from order.const import (
    PayWayError,
    GoodsNotEnough,
    GoodsSellOut,
    UserBalanceNotEnough,
    CanNotBuySelfGoods,
    PayOrderSuccess,
    GoodsNotExist
)
from common.helpers import paged_items
from goods.forms.return_goods_form import ReturnGoodsForm
from common.helpers import d0, dec
from clbauth.help import (
    check_user_login, check_web_enter
)
from django.http import HttpResponseRedirect


@check_web_enter
@check_user_login
def pay_order_info(request):
    user_id = int(request.session.get("user_id"))
    goods_id = int(request.POST.get("goods_id", 41))
    goods_quantity = int(request.POST.get("goods_quantity", 1))
    address_id = int(request.POST.get("address_id", 0))
    pay_asset_name = request.POST.get("pay_asset_name", "BTC")
    eth_unit_coin_amount = request.POST.get("eth_unit_coin_amount", 0)
    usdt_unit_coin_amount = request.POST.get("usdt_unit_coin_amount", 0)
    goods_detail = Goods.objects.filter(id=goods_id).first()
    if pay_asset_name == "ETH":
        pay_coin_amount = eth_unit_coin_amount
    elif pay_asset_name == "USDT":
        pay_coin_amount = usdt_unit_coin_amount
    else:
        pay_coin_amount = d0
    if address_id in ["0", 0, None, ""]:
        tip_msg = "您还没有收货地址, 请点击上方的创建地址按钮去创建"
        return HttpResponseRedirect(str(goods_id) + '/goods_detail?tip_msg=' + tip_msg)
    if pay_asset_name not in ["USDT", "ETH"]:
        tip_msg = "支付方式错误,请选择支付方式"
        return HttpResponseRedirect(str(goods_id) + '/goods_detail?tip_msg=' + tip_msg)
    if goods_detail.left_amount <= 0:
        tip_msg = "商品已经售磬"
        return HttpResponseRedirect(str(goods_id) + '/goods_detail?tip_msg=' + tip_msg)
    if goods_detail.left_amount < goods_quantity:
        tip_msg = "商品数量不足"
        return HttpResponseRedirect(str(goods_id) + '/goods_detail?tip_msg=' + tip_msg)
    user_wallet = UserWallet.objects.filter(
        user__id=user_id, asset__name=pay_asset_name
    ).first()
    if user_wallet.balance < dec(pay_coin_amount) * dec(goods_quantity):
        tip_msg = "您的钱包余不足，请去充值"
        return HttpResponseRedirect(str(goods_id) + '/goods_detail?tip_msg=' + tip_msg)
    auth_user = AuthUser.objects.get(id=user_id)
    if user_wallet.user == goods_detail.merchant.user:
        tip_msg = "不能购买自己发布的商品"
        return HttpResponseRedirect(str(goods_id) + '/goods_detail?tip_msg=' + tip_msg)
    user_address = UserAddress.objects.filter(id=address_id).first()
    total_pay_out = dec(goods_quantity) * dec(pay_coin_amount)
    return render(request, "front/order/create_order.html", locals())


@check_web_enter
@check_user_login
def create_pay_order(request):
    goods_id = int(request.POST.get("goods_id", 0))
    address_id = int(request.POST.get("address_id", 0))
    goods_quantity = int(request.POST.get("goods_quantity", 1))
    pay_asset_name = request.POST.get("pay_asset_name", "ETH")
    eth_unit_coin_amount = request.POST.get("eth_unit_coin_amount", 0)
    usdt_unit_coin_amount = request.POST.get("usdt_unit_coin_amount", 0)
    buyer_id = int(request.session.get("user_id", 0))
    if address_id in ["0", 0, None, ""]:
        tip_msg = "您还没有收货地址, 请点击上方的创建地址按钮去创建"
        return HttpResponseRedirect(str(goods_id) + '/goods_detail?tip_msg=' + tip_msg)
    if pay_asset_name == "ETH":
        unit_coin_amount = dec(eth_unit_coin_amount)
    elif pay_asset_name == "USDT":
        unit_coin_amount = dec(usdt_unit_coin_amount)
    else:
        unit_coin_amount = d0
    order_ret = create(
        goods_id=goods_id,
        goods_quantity=goods_quantity,
        pay_asset_name=pay_asset_name,
        pay_coin_amount=unit_coin_amount,
        buyer_id=buyer_id,
        address_id=address_id,
    )
    goods_detail = Goods.objects.filter(id=goods_id).first()
    if order_ret == GoodsNotExist:
        tip_msg = "您购买的商品不存在"
        return HttpResponseRedirect(str(goods_id)+'/goods_detail?tip_msg='+tip_msg)
    if order_ret == PayWayError:
        tip_msg = "支付方式错误,请选择支付方式"
        return HttpResponseRedirect(str(goods_id) + '/goods_detail?tip_msg=' + tip_msg)
    if order_ret == GoodsNotEnough:
        tip_msg = "商品数量不足"
        return HttpResponseRedirect(str(goods_id) + '/goods_detail?tip_msg=' + tip_msg)
    if order_ret == GoodsSellOut:
        tip_msg = "商品已经售磬"
        return HttpResponseRedirect(str(goods_id)+'/goods_detail?tip_msg='+tip_msg)
    if order_ret == UserBalanceNotEnough:
        tip_msg = "您的钱包余不足，请去充值"
        return HttpResponseRedirect(str(goods_id)+'/goods_detail?tip_msg='+tip_msg)
    if order_ret == CanNotBuySelfGoods:
        tip_msg = "不能购买自己发布的商品"
        return HttpResponseRedirect(str(goods_id)+'/goods_detail?tip_msg='+tip_msg)
    if order_ret == PayOrderSuccess:
        return redirect("order_list")


@check_web_enter
@check_user_login
def order_list(request):
    side_bar = "order_list"
    nav_active = 'order'
    user_id = int(request.session.get("user_id"))
    status = int(request.GET.get("status", 0))
    order_list = GoodsOrder.objects.filter(user__id=user_id).order_by("-id")
    if status in ["1", 1]:  # 待发货
        order_list = order_list.filter(status="PAY_SUCCESS")
    if status in ["2", 2]:  # 待收货
        order_list = order_list.filter(status="SEND_GOODS")
    if status in ["3", 3]:  # 待评价
        order_list = order_list.filter(status="RECV_GOODS")
    if status in ["4", 4]:  # 已完成
        order_list = order_list.filter(status="FINISH")
    order_list = paged_items(request, order_list)
    return render(request, "front/order/order_list.html", locals())


@check_web_enter
@check_user_login
def order_detail(request, id):
    side_bar = "order_list"
    user_id = int(request.session.get("user_id"))
    window = request.GET.get("window", "unknown")
    auth_user = AuthUser.objects.get(id=user_id)
    order_dtl = GoodsOrder.objects.filter(id=int(id)).first()
    order_return = OrederReturn.objects.filter(order=order_dtl).first()
    if order_dtl.status == "RETURN_GOODS":
        return_goods = True
    else:
        return_goods = False
    return render(request, "front/order/order_detail.html", locals())


# 订单退换货
@check_web_enter
@check_user_login
def return_order(request, oid):
    user_id = int(request.session.get("user_id"))
    oid = oid
    red_url = str(oid) + '/order_detail'
    order = GoodsOrder.objects.filter(id=oid).order_by("-id").first()
    if order.status == "RETURN_GOODS":
        return redirect("order_detail", oid)
    if request.method == "GET":
        return_goods_form = ReturnGoodsForm(request)
        return render(request, "front/order/return_order.html", locals())
    if request.method == "POST":
        return_goods_form = ReturnGoodsForm(request, request.POST, request.FILES)
        if return_goods_form.is_valid():
            order.status = OrderStatus.RETURN_GOODS.value
            if order.status == "SEND_GOODS":
                return_goods_form.save_return_data(order, "Yes")
            else:
                return_goods_form.save_return_data(order, "No")
            order.save()
            return redirect("order_detail", oid)
        else:
            error = return_goods_form.errors
            return render(request, 'front/order/return_order.html', {'return_goods_form': return_goods_form, 'error': error})
    return redirect("order_detail", oid)


# 确认收货
@check_web_enter
@check_user_login
def confirm_recv_goods(request, oid):
    red_url = str(oid) + '/order_detail'
    order = GoodsOrder.objects.filter(id=oid).order_by("-id").first()
    order.status = "RECV_GOODS"
    order.save()
    return redirect("order_detail", oid)


# 取消订单退换货(订单回到原始状态)
@check_web_enter
@check_user_login
def cancle_return_order(request, oid):
    red_url = str(oid) + '/order_detail'
    order = GoodsOrder.objects.filter(id=oid).order_by("-id").first()
    order_return = OrederReturn.objects.filter(order=order).first()
    if order_return is not None:
        order.status = order_return.ret_order_status
        order.save()
        order_return.process = "CANCLE_RETURN_GOODS"
        order_return.save()
    return redirect("order_detail", oid)


# 退货货的邮寄订单号添加
@check_web_enter
@check_user_login
def set_orde_shipnum(request, oid):
    ship_company = request.POST.get("ship_company", "")
    ship_number = request.POST.get("ship_number", "")
    order = GoodsOrder.objects.filter(id=oid).order_by("-id").first()
    order.ret_logistics = ship_company
    order.ret_ship_number = ship_number
    order.save()
    return redirect("order_detail", oid)

# 订单退换货申述
@check_web_enter
@check_user_login
def return_orde_approval(request, oid):
    approval = request.POST.get("approval", "")
    order = GoodsOrder.objects.filter(id=oid).order_by("-id").first()
    order_return = OrederReturn.objects.filter(order=order).first()
    order_return.adjust_content = approval
    order_return.save()
    return redirect("order_detail", oid)

# 删除订单
@check_web_enter
@check_user_login
def del_order(request, oid):
    GoodsOrder.objects.filter(id=oid).delete()
    return redirect('order_list')
