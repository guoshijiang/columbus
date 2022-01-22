# encoding=utf-8

from django.shortcuts import redirect, render, reverse
from common.helpers import d0, dec, paged_items
from marchant.models import Marchant
from goods.models import (
    Goods,
    GoodsComment,
    GoodsSate,
    GoodsCat
)
from backend.forms.goods_form import GdsCatForms, StateForms
from backend.helper import check_admin_login


@check_admin_login
def b_goods_list(request):
    self_bar = "goods"
    marchant_name = request.GET.get("marchant_name", "all")
    goods_type = request.GET.get("goods_type", "all")
    mct_list = Marchant.objects.all().order_by("-id")
    gds_list = Goods.objects.all().order_by("-id")
    if marchant_name not in ["", None, "None", "all"]:
        marchant = mct_list.filter(name=marchant_name).first()
        gds_list = gds_list.filter(merchant=marchant)
    if goods_type not in ["", None, "None", "all"]:
        if goods_type == "real":
            gds_list = gds_list.filter(goods_type="实体商品")
        if goods_type == "virtual":
            gds_list = gds_list.filter(goods_type="虚拟商品")
    gds_list = paged_items(request, gds_list)
    return render(request, "backend/goods/goods_list.html", locals())

@check_admin_login
def b_goods_detail(request, gid):
    self_bar = "goods"
    gds_dtl = Goods.objects.filter(id=gid).first()
    return render(request, "backend/goods/goods_detail.html", locals())

@check_admin_login
def disable_goods(request, gid):
    goods = Goods.objects.filter(id=gid).first()
    goods.is_active = False
    goods.save()
    return redirect("goods_list")

@check_admin_login
def enable_goods(request, gid):
    goods = Goods.objects.filter(id=gid).first()
    goods.is_active = True
    goods.save()
    return redirect("goods_list")

@check_admin_login
def b_goods_comment_list(request, gid):
    goods_id = gid
    gds_cmt_list = GoodsComment.objects.filter(goods__id=gid).order_by("-id")
    gds_cmt_list = paged_items(request, gds_cmt_list)
    return render(request, "backend/goods/goods_comment_list.html", locals())


@check_admin_login
def b_goods_cat(request):
    self_bar = "goods"
    gcat_list = GoodsCat.objects.all().order_by("-id")
    return render(request, "backend/goods/goods_cat/b_goods_cat.html", locals())


@check_admin_login
def create_bgoods_cat(request):
    self_bar = "goods"
    if request.method == "GET":
        gcat_form = GdsCatForms(request)
        return render(request, "backend/goods/goods_cat/create_bgds_cat.html", locals())
    if request.method == "POST":
        gcat_form = GdsCatForms(request, request.POST)
        if gcat_form.is_valid():
            gcat_form.create_gds_cat()
            return redirect("b_goods_cat")
        else:
            error = gcat_form.errors
            return render(
                request,
                "backend/goods/goods_cat/create_bgds_cat.html",
                {
                    'gcat_form': gcat_form,
                    'error': error
                }
            )

@check_admin_login
def update_bgoods_cat(request, cid):
    self_bar = "goods"
    gcat = GoodsCat.objects.filter(id=cid).first()
    cat_id = cid
    if request.method == "GET":
        gcat_form = GdsCatForms(request, instance=gcat)
        return render(request, "backend/goods/goods_cat/update_bgds_cat.html", locals())
    if request.method == "POST":
        gcat_form = GdsCatForms(request, request.POST, instance=gcat)
        if gcat_form.is_valid():
            gcat_form.update_gds_cat(cid)
            return redirect("b_goods_cat")
        else:
            error = gcat_form.errors
            return render(
                request,
                "backend/goods/goods_cat/update_bgds_cat.html",
                {
                    'gcat_form': gcat_form,
                    'error': error
                }
            )


@check_admin_login
def delete_bgoods_cat(request, cid):
    GoodsCat.objects.filter(id=cid).delete()
    return redirect("b_goods_cat")


@check_admin_login
def b_goods_state(request):
    self_bar = "goods"
    gstate_list = GoodsSate.objects.all().order_by("-id")
    return render(request, "backend/goods/goods_state/b_goods_state.html", locals())


@check_admin_login
def create_bgoods_state(request):
    self_bar = "goods"
    if request.method == "GET":
        gstate_form = StateForms(request)
        return render(request, "backend/goods/goods_state/create_bgds_state.html", locals())
    if request.method == "POST":
        gstate_form = StateForms(request, request.POST)
        if gstate_form.is_valid():
            gstate_form.create_state()
            return redirect("b_goods_state")
        else:
            error = gstate_form.errors
            return render(
                request,
                "backend/goods/goods_state/create_bgds_state.html",
                {
                    'gstate_form': gstate_form,
                    'error': error
                }
            )


@check_admin_login
def update_bgoods_state(request, sid):
    self_bar = "goods"
    gstate = GoodsSate.objects.filter(id=sid).first()
    state_id = sid
    if request.method == "GET":
        gstate_form = StateForms(request, instance=gstate)
        return render(request, "backend/goods/goods_state/update_bgds_state.html", locals())
    if request.method == "POST":
        gstate_form = StateForms(request, request.POST, instance=gstate)
        if gstate_form.is_valid():
            gstate_form.update_state(sid)
            return redirect("b_goods_state")
        else:
            error = gstate_form.errors
            return render(
                request,
                "backend/goods/goods_state/update_bgds_state.html",
                {
                    'gstate_form': gstate_form,
                    'error': error
                }
            )


@check_admin_login
def delete_bgoods_state(request, sid):
    GoodsSate.objects.filter(id=sid).delete()
    return redirect("b_goods_state")


