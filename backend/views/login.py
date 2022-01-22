# encoding=utf-8

import pytz
from django.shortcuts import render, redirect
from backend.models import AdminUser
from backend.helper import check_admin_login

def b_login(request):
    name = request.POST.get("name", "")
    password = request.POST.get("password", "")
    admin_user = AdminUser.objects.filter(name=name).first()
    if admin_user is None:
        tip_msg = "用户不存在,请检查之后再登陆"
        return render(request, "backend/login.html", locals())
    if admin_user.password == password:
        request.session["backend_login"] = True
        return redirect("b_index")
    else:
        tip_msg = "密码错误,请检查之后再登陆"
        return render(request, "backend/login.html", locals())


@check_admin_login
def b_logout(request):
    request.session["backend_login"] = False
    request.session.flush()
    return render(request, "backend/login.html", locals())





