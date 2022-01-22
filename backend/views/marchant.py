# encoding=utf-8

from django.shortcuts import redirect, render, reverse
from common.helpers import d0, dec, paged_items
from marchant.models import (
    Marchant,
    MarchantStat,
    MarchantOrderFlow,
    MarchantOpenRecord
)
from backend.helper import check_admin_login
from goods.models import Goods


@check_admin_login
def b_marchants_list(request):
    self_bar = "marchant"
    marchant_name = request.GET.get("marchant_name", "")
    mct_list = Marchant.objects.all().order_by("-id")
    if marchant_name not in ["", None, "None", "all"]:
        mct_list = mct_list.filter(name__icontains=marchant_name)
    mct_list = paged_items(request, mct_list)
    return render(request, "backend/marchant/marchant_list.html", locals())

@check_admin_login
def b_marchant_detail(request, mid):
    self_bar = "marchant"
    marchant = Marchant.objects.filter(id=mid).first()
    return render(request, "backend/marchant/marchant_detail.html", locals())

@check_admin_login
def open_marchant_list(request):
    self_bar = "marchant"
    marchant_name = request.GET.get("marchant_name", "all")
    mct_list = Marchant.objects.all().order_by("-id")
    open_record_list = MarchantOpenRecord.objects.all().order_by("-id")
    if marchant_name not in ["", None, "None", "all"]:
        marchant = mct_list.filter(name=marchant_name).first()
        open_record_list = open_record_list.filter(marchant=marchant)
    open_record_list = paged_items(request, open_record_list)
    return render(request, "backend/marchant/open_marchant_list.html", locals())

@check_admin_login
def b_marchant_flow(request):
    self_bar = "marchant"
    marchant_name = request.GET.get("marchant_name", "all")
    mct_list = Marchant.objects.all().order_by("-id")
    flow_list = MarchantOrderFlow.objects.all().order_by("-id")
    if marchant_name not in ["", None, "None", "all"]:
        marchant = mct_list.filter(name=marchant_name).first()
        flow_list = flow_list.filter(marchant=marchant)
    flow_list = paged_items(request, flow_list)
    return render(request, "backend/marchant/marchant_flow.html", locals())

@check_admin_login
def disable_marchant(request, mid):
    marchant = Marchant.objects.filter(id=mid).first()
    marchant.is_active = False
    marchant.save()
    gds_list = Goods.objects.filter(merchant=marchant)
    for gds in gds_list:
        gds.is_active = False
        gds.save()
    return redirect("b_marchants_list")

@check_admin_login
def enable_marchant(request, mid):
    marchant = Marchant.objects.filter(id=mid).first()
    marchant.is_active = True
    marchant.save()
    gds_list = Goods.objects.filter(merchant=marchant)
    for gds in gds_list:
        gds.is_active = True
        gds.save()
    return redirect("b_marchants_list")

@check_admin_login
def update_mct_settle(request, mid):
    self_bar = "marchant"
    marchant = Marchant.objects.filter(id=mid).first()
    if request.method == "GET":
        return render(request, "backend/marchant/marchant_upd_settle.html", locals())
    if request.method == "POST":
        settle_percent = request.POST.get("settle_percent", d0)
        marchant.settle_percent = dec(settle_percent)
        marchant.save()
        return redirect("marchant_detail", mid)

@check_admin_login
def marchant_cmt_data(request, mid):
    self_bar = "marchant"
    marchant_id = mid
    mct_stat_data = MarchantStat.objects.filter(marchant__id=mid)
    return render(request, "backend/marchant/marchant_cmt_data.html", locals())


