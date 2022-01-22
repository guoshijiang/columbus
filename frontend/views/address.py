# encoding=utf-8

import pytz
from django.conf import settings
from django.db.models import F, Q
from django.shortcuts import redirect, render, reverse
from clbauth.forms.address_form import UseAddressForm
from clbauth.models import UserAddress, AuthUser
from common.helpers import d0, dec, paged_items
from clbauth.help import (
    check_user_login, check_web_enter
)

@check_web_enter
@check_user_login
def add_address(request):
    user_id = request.session.get("user_id")
    side_bar = "address_list"
    if request.method == "GET":
        addr_from = UseAddressForm(request)
        return render(request, "front/address/add_address.html", locals())
    if request.method == "POST":
        addr_from = UseAddressForm(request, request.POST)
        if addr_from.is_valid():
            addr_from.save_addr(user_id)
            return redirect('address_list')
        else:
            error = addr_from.errors
            return render(request, 'front/address/add_address.html', {'addr_from': addr_from, 'error': error})

@check_web_enter
@check_user_login
def update_address(request, aid):
    user_addr = UserAddress.objects.filter(id=aid).order_by("-id").first()
    side_bar = "address_list"
    if request.method == "GET":
        addr_from = UseAddressForm(request, instance=user_addr)
        return render(request, "front/address/update_address.html", locals())
    if request.method == "POST":
        addr_from = UseAddressForm(request, request.POST)
        if addr_from.is_valid():
            addr_from.update_addr(user_addr.id)
            return redirect('address_list')
        else:
            error = addr_from.errors
            return render(request, 'front/address/update_address.html', {'addr_from': addr_from, 'error': error})
    return redirect("address_list")


@check_web_enter
@check_user_login
def address_list(request):
    user_id = request.session.get("user_id")
    side_bar = "address_list"
    user = AuthUser.objects.filter(id=user_id).first()
    ret_address_list = UserAddress.objects.filter(user=user).order_by("-id")
    ret_address_list = paged_items(request, ret_address_list)
    return render(request, "front/address/address_list.html", locals())


@check_web_enter
@check_user_login
def del_address(request, aid):
    UserAddress.objects.filter(id=aid).delete()
    return redirect("address_list")
