#encoding=utf-8

from django.shortcuts import redirect, render


def check_admin_login(func):
    def admin_user(request, *args, ** kwargs):
        if request.session.get("backend_login") is False\
                or request.session.get("backend_login") is None:
            return redirect("b_login")
        return func(request, *args, **kwargs)
    return admin_user