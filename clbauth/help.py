#encoding=utf-8

import random
import hashlib
import json
from django.shortcuts import redirect, render


def get_code(number=6, alpha=False):
    verify_code = ''
    for i in range(number):
        num = random.randint(0, 9)
        if alpha is True:
            upper_alpha = chr(random.randint(65, 90))
            lower_alpha = chr(random.randint(97, 122))
            num = random.choice([num, upper_alpha, lower_alpha])
        verify_code = verify_code + str(num)
    return verify_code


def hash_code(s, salt='mysite_login'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def check_user_login(func):
    def user_auth(request, *args, ** kwargs):
        if request.session.get("is_login") is False\
                or request.session.get("is_login") is None:
            return redirect("before_login")
        return func(request, *args, **kwargs)
    return user_auth


def check_web_enter(func):
    def user_auth(request, *args, **kwargs):
        if request.session.get("checked") is False \
                or request.session.get("checked") is None:
            return redirect("/")
        return func(request, *args, **kwargs)
    return user_auth