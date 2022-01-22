# encoding=utf-8

import logging
from django.shortcuts import redirect, render, reverse
from marchant.models import MarchantConfig
from backend.forms.mct_open_config import MarchantOpneForm
from backend.helper import check_admin_login


@check_admin_login
def mct_config_list(request):
    self_bar = "marchant"
    mct_con_list = MarchantConfig.objects.all().order_by("-id")
    return render(request, "backend/config/mct_config_list.html", locals())


@check_admin_login
def create_mct_config(request):
    self_bar = "marchant"
    if request.method == "GET":
        mct_open_form = MarchantOpneForm(request)
        return render(request, "backend/config/create_mct_config.html", locals())
    if request.method == "POST":
        mct_open_form = MarchantOpneForm(request, request.POST)
        if mct_open_form.is_valid():
            mct_open_form.create_config()
            return redirect("mct_config_list")
        else:
            error = mct_open_form.errors
            return render(
                request,
                "backend/config/create_mct_config.html",
                {
                    'mct_open_form': mct_open_form,
                    'error': error
                }
            )


@check_admin_login
def update_mct_config(request, cid):
    self_bar = "marchant"
    marchant_config = MarchantConfig.objects.filter(id=cid).first()
    config_id = cid
    if request.method == "GET":
        mct_open_form = MarchantOpneForm(request, instance=marchant_config)
        return render(request, "backend/config/update_mct_config.html", locals())
    if request.method == "POST":
        mct_open_form = MarchantOpneForm(request, request.POST, instance=marchant_config)
        if mct_open_form.is_valid():
            mct_open_form.update_config(cid)
            return redirect("mct_config_list")
        else:
            error = mct_open_form.errors
            return render(
                request,
                "backend/config/update_mct_config.html",
                {
                    'mct_open_form': mct_open_form,
                    'error': error
                }
            )
