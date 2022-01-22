# encoding=utf-8
import logging

import pytz
import time
from django.db import transaction
from django.conf import settings
from django.db.models import F, Q
from django.shortcuts import redirect, render, reverse
from common.helpers import d0, dec, paged_items
from common.models import Asset
from frontend.views.utils.base import keep_four, keep_two
from goods.models import (
    Goods, GoodsOrder, OrederReturn, GoodsComment, GoodsImage
)
from marchant.models import (
    Marchant,
    MarchantConfig,
    MarchantStat,
    MarchantOrderFlow,
    MarchantCollect,
    MarchantBackList,
    MarchantOpenRecord
)
from clbauth.models import AuthUser, UserWallet, TansRecord
from marchant.forms.marchant_form import MarchantOpenForm
from marchant.consts import UserWalletBalanceNotEnough, AlreadyOpendMarchant, OpenMarchantSuccess
from marchant.forms.goods_form import RealGoodsForm, VitualGoodsForm
from django.http import HttpResponseRedirect
from clbauth.help import (
    check_user_login, check_web_enter
)
from django.core.files.base import ContentFile


@check_web_enter
@check_user_login
def marchants_list(request):
    nav_active = 'marchant'
    marchant_name = request.POST.get("marchant_name", None)
    marchant_list = Marchant.objects.filter(is_active=True).order_by("-id")
    if marchant_name not in ["", None]:
        marchant_list = marchant_list.filter(name__contains=marchant_name)
    marchant_list = paged_items(request, marchant_list)
    return render(request, "front/marchant/marchant_list.html", locals())


@check_web_enter
@check_user_login
def marchants_detail(request, id):
    nav_active = 'marchant'
    marchant_detail = Marchant.objects.filter(id=id).first()
    side_bar = "become_marchant"
    marchant_goods_lst = Goods.objects.filter(merchant=marchant_detail)
    marchant_goods_lst = paged_items(request, marchant_goods_lst)
    return render(request, "front/marchant/marchant_detail.html", locals())


@check_web_enter
@check_user_login
def update_marchant(request, mid):
    user_id = request.session.get("user_id")
    user = AuthUser.objects.filter(id=user_id).first()
    marchant_detail = Marchant.objects.filter(id=mid).first()
    if request.method == "GET":
        marchant_form = MarchantOpenForm(request, user, instance=marchant_detail)
        return render(request, "front/marchant/update_marchant.html", locals())
    if request.method == "POST":
        marchant_form = MarchantOpenForm(request, user, request.POST, request.FILES, instance=marchant_detail)
        if marchant_form.is_valid():
            marchant_form.update_marchant(marchant_detail.id)
            return redirect('self_marchant_detail')
        else:
            error = marchant_form.errors
            return render(
                request, "front/marchant/marchant_add_info.html",
                {'user': user, 'marchant_form': marchant_form, 'error': error}
            )


@check_web_enter
@check_user_login
def become_marchant(request):
    nav_active = 'marchant'
    user_id = request.session.get("user_id")
    mct_config = MarchantConfig.objects.filter(config_type='Marchant').first()
    if mct_config is None:
        return render(request, "front/marchant/become_marchant.html", locals())
    user = AuthUser.objects.filter(id=user_id).first()
    marchant = Marchant.objects.filter(user__id=user_id).first()
    if user.is_merchant == "Yes" and marchant is not None:
        return redirect("self_marchant_detail")
    elif user.is_merchant == "Yes" and marchant is None:
        return redirect("create_marchant")
    else:
        return render(request, "front/marchant/become_marchant.html", locals())


@check_web_enter
@check_user_login
@transaction.atomic
def open_marchant(request):
    nav_active = 'marchant'
    user = AuthUser.objects.filter(id=int(request.session.get("user_id"))).first()
    mct_config = MarchantConfig.objects.filter(config_type='Marchant').first()
    if request.method == "GET":
        open_marchant_req_way = "GET"
        pay_way = request.GET.get("pay_way", None)
        asset = Asset.objects.filter(name=pay_way).order_by("-id").first()
        user_wallet = UserWallet.objects.filter(
            user=user,
            asset=asset
        ).order_by("-id").first()
        wallet_amount = user_wallet.balance
        pay_amount = mct_config.eth_amount if pay_way == "ETH" else mct_config.usdt_amount
        if wallet_amount < pay_amount:
            balance = "NotEnough"
            deposit_amount = pay_amount - wallet_amount
        else:
            wallet_left_amount = wallet_amount - pay_amount
            open_marchant_req_way = "POST"
        return render(request, "front/marchant/become_marchant.html", locals())
    if request.method == "POST":
        pay_way = request.POST.get("pay_way", None)
        user = AuthUser.objects.filter(id=int(request.session.get("user_id"))).first()
        mct_config = MarchantConfig.objects.filter(config_type='Marchant').first()
        marchant = Marchant.objects.filter(user=user).first()
        if user.is_merchant == "Yes" and marchant is None:
            return redirect("create_marchant")
        elif user.is_merchant == "Yes" and marchant is not None:
            return redirect("create_marchant")
        else:
            asset = Asset.objects.filter(name=pay_way).first()
            user_wallet = UserWallet.objects.filter(
                user=user, asset=asset
            ).order_by("-id").first()
            if pay_way == "ETH":
                pay_mount_db = mct_config.eth_amount
            else:
                pay_mount_db = mct_config.usdt_amount
            user_wallet.balance = user_wallet.balance - pay_mount_db
            user_wallet.out_amount = user_wallet.out_amount + pay_mount_db
            user_wallet.save()
            MarchantOpenRecord.objects.create(
                user=user,
                pay_coin_amount=pay_mount_db,
                pay_way=pay_way,
                pay_at=time.time()
            )
            TansRecord.objects.create(
                user=user,
                asset=asset,
                amount=pay_mount_db,
                trans_way="Output",
                source="开通商家支出"
            )
            user.is_merchant = "Yes"
            user.save()
            return redirect("create_marchant")


@check_web_enter
@check_user_login
def create_marchant(request):
    nav_active = 'marchant'
    user_id = request.session.get("user_id")
    user = AuthUser.objects.filter(id=user_id).first()
    if request.method == "GET":
        mct_open_form = MarchantOpenForm(request, user)
        return render(request, "front/marchant/marchant_add_info.html", locals())
    if request.method == "POST":
        mct_open_form = MarchantOpenForm(request, user, request.POST, request.FILES)
        if mct_open_form.is_valid():
            mct_logo = request.FILES.get("logo", "")
            create_marchant = Marchant.objects.create(
                user=user,
                name=mct_open_form.clean_name(),
                introduce=mct_open_form.clean_introduce(),
                detail=mct_open_form.clean_detail(),
            )
            MarchantOpenRecord.objects.filter(user=user).update(marchant=create_marchant)
            file_content = ContentFile(mct_logo.read())
            create_marchant.logo.save(mct_logo.name, file_content)
            MarchantStat.objects.create(
                marchant=create_marchant,
            )
            return redirect("self_marchant_detail")
        else:
            error = mct_open_form.errors
            return render(
                request, "front/account/update_pin.html",
                {'user': user, 'mct_open_form': mct_open_form, 'error': error}
            )


@check_web_enter
@check_user_login
def self_marchant_detail(request):
    nav_active = 'marchant'
    user_id = request.session.get("user_id")
    user = AuthUser.objects.filter(id=user_id).first()
    if user.is_merchant is None:
        return redirect("before_login")
    else:
        marchant = Marchant.objects.filter(user=user).order_by("-id").first()
        marchant_stdata = MarchantStat.objects.filter(marchant=marchant).order_by("-id").first()
        # 商品统计
        selling_goods = Goods.objects.filter(merchant=marchant, is_sale='Yes', left_amount__gt=0).count()
        selled_goods = Goods.objects.filter(merchant=marchant).filter(left_amount__lt=0).count()
        sale_goods = Goods.objects.filter(merchant=marchant).filter(is_sale='No').count()
        # 订单统计
        total_goods_order = GoodsOrder.objects.filter(merchant=marchant).count()
        total_wait_send_num = GoodsOrder.objects.filter(merchant=marchant, status='PAY_SUCCESS').count()
        total_sent_num = GoodsOrder.objects.filter(merchant=marchant, status='SEND_GOODS').count()
        total_wait_handle_num = GoodsOrder.objects.filter(merchant=marchant, status='RETURN_GOODS').count()
        total_wait_retmoneye_num = GoodsOrder.objects.filter(
            Q(merchant=marchant),
            Q(status='APPOVAL_SUCCESS') | Q(status='RETURN_SELLER_ACPT')
        ).count()
        total_finish_num = GoodsOrder.objects.filter(merchant=marchant, status='FINISH').count()
        # 结算统计
        total_amount = d0
        settle_amount = d0
        unsettle_amount = d0
        valid_amount = d0
        invalid_amount = d0
        mct_flow_list = MarchantOrderFlow.objects.filter(marchant=marchant, is_active=True).order_by("-id")
        for mct_flow in mct_flow_list:
            total_amount += mct_flow.coin_amount
            if mct_flow.is_valid == 'Yes':
                valid_amount += mct_flow.coin_amount
            if mct_flow.is_valid == 'No':
                invalid_amount += mct_flow.coin_amount
            if mct_flow.is_stat == 'Yes':
                settle_amount += mct_flow.coin_amount
            if mct_flow.is_stat == "No":
                unsettle_amount += mct_flow.coin_amount
    return render(request, "front/marchant/self_marchant_detail.html", locals())


@check_web_enter
@check_user_login
def marchant_add_goods(request):
    nav_active = 'marchant'
    user_id = request.session.get("user_id")
    user = AuthUser.objects.filter(id=user_id).first()
    goods_type = request.GET.get("goods_type", "real")
    marchant = Marchant.objects.filter(user=user).order_by("-id").first()
    if request.method == "GET":
        if goods_type == "real":
            goods_form = RealGoodsForm(request, marchant)
        else:
            goods_form = VitualGoodsForm(request, marchant)
        return render(request, "front/marchant/goods/add_goods.html", locals())
    if request.method == "POST":
        if goods_type == "real":
            goods_type_zh = "实体商品"
            goods_form = RealGoodsForm(request, marchant, request.POST)
        else:
            goods_type_zh = "虚拟商品"
            goods_form = VitualGoodsForm(request, marchant, request.POST)
        if goods_form.is_valid():
            gds = goods_form.create_goods(goods_type_zh)
            return HttpResponseRedirect('/goods_images_update?goods_id=' + str(gds.id))
        else:
            error = goods_form.errors
            return render(
                request, "front/marchant/goods/add_goods.html",
                {
                    'user': user,
                    'marchant': marchant,
                    'goods_form': goods_form,
                    'goods_type': goods_type,
                    'error': error
                }
            )


@check_web_enter
@check_user_login
def goods_images_update(request):
    nav_active = 'marchant'
    user_id = request.session.get("user_id")
    user = AuthUser.objects.filter(id=user_id).first()
    tip_msg = request.GET.get("tip_msg", "")
    marchant = Marchant.objects.filter(user=user).order_by("-id").first()
    if request.method == "GET":
        goods_id = request.GET.get("goods_id")
        to_list = request.GET.get("to_list", "No")
        gds = Goods.objects.filter(id=goods_id).first()
        if gds is None:
            tip_msg = "该商品不存在, 请返回到商品添加页面添加商品"
            return render(request, "front/marchant/goods/goods_images_upload.html", locals())
        if to_list == "Yes":
            if gds.logo not in [None, "None"]:
                return redirect("marchant_goods_list")
            else:
                tip_msg = "您还没有上传商品图片，至少需要上传一张商品图片"
        return render(request, "front/marchant/goods/goods_images_upload.html", locals())
    if request.method == "POST":
        goods_id = request.POST.get("goods_id")
        goods_img = request.FILES.get("goods_img")
        gds = Goods.objects.filter(id=goods_id).first()
        if gds is not None and goods_img is not None:
            gds_img = GoodsImage(image=goods_img)
            gds_img.save()
            gds.logo = gds_img
            gds.save()
            gds.goods_image.add(gds_img)
            return HttpResponseRedirect('/goods_images_update?goods_id=' + str(gds.id))
        else:
            tip_msg = "您没有上传商品图片或该商品不存在"
            return HttpResponseRedirect('/goods_images_update?goods_id=' + str(goods_id) + "&tip_msg=" + tip_msg)

@check_web_enter
@check_user_login
def delele_goods_image(request, gid):
    img_id = request.GET.get("img_id")
    print("img_id = ", img_id)
    goods_img = GoodsImage.objects.filter(id=img_id).first()
    goods = Goods.objects.filter(id=gid).first()
    if int(goods.logo.id) == int(img_id):
        goods.logo = None
        goods.save()
    goods.goods_image.remove(goods_img)
    return HttpResponseRedirect('/goods_images_update?goods_id=' + str(goods.id))


@check_web_enter
@check_user_login
def marchant_upd_goods(request, gid):
    nav_active = 'marchant'
    user_id = request.session.get("user_id")
    user = AuthUser.objects.filter(id=user_id).first()
    goods_type = request.GET.get("goods_type", "real")
    marchant = Marchant.objects.filter(user=user).order_by("-id").first()
    gds = Goods.objects.filter(id=gid).first()
    if gds.goods_type in ["实体商品", "real"]:
        goods_type = "real"
    else:
        goods_type = "virtual"
    if request.method == "GET":
        print("goods_type ==", goods_type)
        if goods_type in ["实体商品", "real"]:
            goods_form = RealGoodsForm(request, marchant, instance=gds)
        else:
            goods_form = VitualGoodsForm(request, marchant, instance=gds)
        return render(request, "front/marchant/goods/upd_goods.html", locals())
    if request.method == "POST":
        if goods_type == "real":
            goods_form = RealGoodsForm(request, marchant, request.POST, instance=gds)
        else:
            goods_form = VitualGoodsForm(request, marchant, request.POST, instance=gds)
        if goods_form.is_valid():
            upd_gds = goods_form.update_goods(gds.id)
            return HttpResponseRedirect('/goods_images_update?goods_id=' + str(gds.id))
        else:
            error = goods_form.errors
            return render(
                request, "front/marchant/goods/upd_goods.html",
                {
                    'user': user,
                    'marchant': marchant,
                    'goods_form': goods_form,
                    'goods_type': goods_type,
                    'error': error
                }
            )


@check_web_enter
@check_user_login
def marchant_goods_list(request):
    nav_active = 'marchant'
    status = request.GET.get("status", 0)
    user_id = request.session.get("user_id")
    user = AuthUser.objects.filter(id=user_id).first()
    marchant = Marchant.objects.filter(user=user).order_by("-id").first()
    selling_goods = Goods.objects.filter(merchant=marchant, is_sale='Yes', left_amount__gt=0).count()
    selled_goods = Goods.objects.filter(merchant=marchant).filter(left_amount=0).count()
    sale_goods = Goods.objects.filter(merchant=marchant).filter(is_sale='No').count()
    goods_list = Goods.objects.filter(merchant=marchant).order_by("-id")
    status_active = "all"
    if status in [1, "1"]:  # 在售
        status_active = "selling"
        goods_list = goods_list.filter(left_amount__gt=0, is_sale="Yes")
    if status in [2, "2"]:  # 售磬
        status_active = "selled"
        goods_list = goods_list.filter(left_amount=0)
    if status in [3, "3"]:  # 已下架
        status_active = "sale"
        goods_list = goods_list.filter(is_sale="No")
    goods_list = paged_items(request, goods_list)
    return render(request, "front/marchant/goods/mct_goods_list.html", locals())


@check_web_enter
@check_user_login
def marchant_goods_sale(request):
    nav_active = 'marchant'
    gid = request.GET.get("gid")
    is_sale = request.GET.get("is_sale")
    Goods.objects.filter(id=gid).update(is_sale=is_sale)
    return redirect("marchant_goods_list")


@check_web_enter
@check_user_login
def marchant_order_list(request, mid):
    nav_active = 'marchant'
    status = int(request.GET.get("status", 0))
    marchant = Marchant.objects.filter(id=mid).first()
    order_list = GoodsOrder.objects.filter(merchant=marchant).order_by("-id")
    if status in ["1", 1]:  # 待发货
        order_list = order_list.filter(status="PAY_SUCCESS")
    if status in ["2", 2]:  # 待收货
        order_list = order_list.filter(status="SEND_GOODS")
    if status in ["3", 3]:  # 待评价
        order_list = order_list.filter(status="RECV_GOODS")
    if status in ["4", 4]:  # 已完成
        order_list = order_list.filter(status="FINISH")
    order_list = paged_items(request, order_list)
    return render(request, "front/marchant/order/marchant_order_list.html", locals())


@check_web_enter
@check_user_login
def marchant_order_detail(request, oid):
    nav_active = 'marchant'
    user_id = int(request.session.get("user_id"))
    window = request.GET.get("window", "unknown")
    auth_user = AuthUser.objects.get(id=user_id)
    marchant = Marchant.objects.filter(user=auth_user).order_by("-id").first()
    order_dtl = GoodsOrder.objects.filter(id=oid).first()
    order_return = OrederReturn.objects.filter(order=order_dtl).first()
    if order_dtl.status == "RETURN_GOODS":
        return_goods = True
    else:
        return_goods = False
    return render(request, "front/marchant/order/marchant_order_detail.html", locals())


@check_web_enter
@check_user_login
def marchant_send_goods(request, oid):
    nav_active = 'marchant'
    ship_company = request.POST.get("ship_company", "")
    ship_number = request.POST.get("ship_number", "")
    order = GoodsOrder.objects.filter(id=oid).order_by("-id").first()
    order.logistics = ship_company
    order.express_number = ship_number
    order.status = "SEND_GOODS"
    order.save()
    return redirect("marchant_order_detail", oid)


@check_web_enter
@check_user_login
def agree_return_goods(request, oid):
    nav_active = 'marchant'
    order = GoodsOrder.objects.filter(id=oid).order_by("-id").first()
    order_return = OrederReturn.objects.filter(order=order).first()
    order_return.process = "RETURN_SELLER_ACPT"
    order_return.save()
    return redirect("marchant_order_detail", oid)


@check_web_enter
@check_user_login
def refuse_return_goods(request, oid):
    nav_active = 'marchant'
    refuse_reason = request.POST.get("refuse_reason", "")
    order = GoodsOrder.objects.filter(id=oid).order_by("-id").first()
    order_return = OrederReturn.objects.filter(order=order).first()
    order_return.process = "RETURN_SELLER_RJT"
    order_return.ret_pay_rs = refuse_reason
    order_return.save()
    return redirect("marchant_order_detail", oid)


@check_web_enter
@check_user_login
@transaction.atomic
def confirm_return_money(request, oid):
    nav_active = 'marchant'
    order = GoodsOrder.objects.filter(id=oid).order_by("-id").first()
    order_return = OrederReturn.objects.filter(order=order).first()
    # 用户钱包加钱
    user_wallet = UserWallet.objects.filter(
        user__id=order.user.id,
        asset__id=order.pay_asset.id
    ).order_by("-id").first()
    user_wallet.balance = user_wallet.balance + order.pay_coin_amount
    user_wallet.save()
    order_return.process = "SELLER_RETURN_MNY"
    order_return.save()
    order.status = "FINISH"
    order.save()
    # 商家流水无效
    marchant_order_flow = MarchantOrderFlow.objects.filter(order_id=order.id).first()
    marchant_order_flow.is_valid = "No"
    marchant_order_flow.save()
    return redirect("marchant_order_detail", oid)


@check_web_enter
@check_user_login
def marchant_comment_list(request, mid):
    nav_active = 'marchant'
    marchant = Marchant.objects.filter(id=mid).order_by("-id").first()
    comment_list = GoodsComment.objects.filter(merchant__id=mid).order_by("-id")
    comment_list = paged_items(request, comment_list)
    return render(request, "front/marchant/marchant_comment_list.html", locals())


@check_web_enter
@check_user_login
def user_marchant_detail(request, mid):
    marchant = Marchant.objects.filter(id=mid).order_by("-id").first()
    marchant_stdata = MarchantStat.objects.filter(marchant=marchant).order_by("-id").first()
    # 商品统计
    selling_goods = Goods.objects.filter(merchant=marchant, is_sale='Yes', left_amount__gt=0).count()
    selled_goods = Goods.objects.filter(merchant=marchant).filter(left_amount__gt=0).count()
    sale_goods = Goods.objects.filter(merchant=marchant).filter(is_sale='No').count()
    # 订单统计
    total_goods_order = GoodsOrder.objects.filter(merchant=marchant).count()
    total_wait_send_num = GoodsOrder.objects.filter(merchant=marchant, status='PAY_SUCCESS').count()
    total_sent_num = GoodsOrder.objects.filter(merchant=marchant, status='SEND_GOODS').count()
    total_wait_handle_num = GoodsOrder.objects.filter(merchant=marchant, status='RETURN_GOODS').count()
    total_wait_retmoneye_num = GoodsOrder.objects.filter(
        Q(merchant=marchant),
        Q(status='APPOVAL_SUCCESS') | Q(status='RETURN_SELLER_ACPT')
    ).count()
    total_finish_num = GoodsOrder.objects.filter(merchant=marchant, status='FINISH').count()
    return render(request, "front/marchant/user_marchant_detail.html", locals())


@check_web_enter
@check_user_login
def collect_marchant(request, mid):
    user_id = request.session.get("user_id")
    auth_user = AuthUser.objects.get(id=user_id)
    marchant = Marchant.objects.filter(id=mid).order_by("-id").first()
    m_clt = MarchantCollect.objects.filter(user=auth_user, marchant=marchant).first()
    if m_clt is None:
        MarchantCollect.objects.create(
            user=auth_user,
            marchant=marchant
        )
    return redirect(collect_list)


@check_web_enter
@check_user_login
def collect_list(request):
    side_bar = "collect_list"
    user_id = request.session.get("user_id")
    m_clt_list = MarchantCollect.objects.filter(user__id=user_id)
    m_clt_list = paged_items(request, m_clt_list)
    return render(request, "front/marchant/marchant_collect_list.html", locals())


@check_web_enter
@check_user_login
def del_collect(request, id):
    MarchantCollect.objects.filter(id=id).delete()
    return redirect(collect_list)


@check_web_enter
@check_user_login
def add_mct_to_blacklist(request, mid):
    user_id = request.session.get("user_id")
    auth_user = AuthUser.objects.get(id=user_id)
    marchant = Marchant.objects.filter(id=mid).order_by("-id").first()
    m_black = MarchantBackList.objects.filter(user=auth_user, marchant=marchant).first()
    if m_black is None:
        MarchantBackList.objects.create(
            user=auth_user,
            marchant=marchant
        )
    return redirect(marchant_black_list)


@check_web_enter
@check_user_login
def marchant_black_list(request):
    side_bar = "marchant_black_list"
    user_id = request.session.get("user_id")
    m_black_list = MarchantBackList.objects.filter(user__id=user_id)
    m_black_list = paged_items(request, m_black_list)
    return render(request, "front/marchant/marchant_black_list.html", locals())


@check_web_enter
@check_user_login
def del_black(request, id):
    MarchantBackList.objects.filter(id=id).delete()
    return redirect(collect_list)


@check_web_enter
@check_user_login
def marchant_settle_flow(request, mid):
    status = int(request.GET.get("status", 0))
    marchant = Marchant.objects.filter(id=mid).order_by("-id").first()
    marchant_flow_list = MarchantOrderFlow.objects.filter(marchant__id=mid).order_by("-id")
    if status in [1, "1"]:
        marchant_flow_list = marchant_flow_list.filter(is_stat='Yes')
    if status in [2, "2"]:
        marchant_flow_list = marchant_flow_list.filter(is_valid='No')
    if status in [3, "3"]:
        marchant_flow_list = marchant_flow_list.filter(is_stat="No", is_valid='Yes')
    for marchant_flow_item in marchant_flow_list:
        order_dtl = GoodsOrder.objects.filter(id=marchant_flow_item.order_id).order_by("-id").first()
        marchant_flow_item.order = order_dtl
    marchant_flow_list = paged_items(request, marchant_flow_list)
    return render(request, "front/marchant/marchant_settle_flow.html", locals())


