# encoding=utf-8

from django.core.cache import cache
from clbauth.forms.enter_form import EnterForm
from django.shortcuts import redirect, render


def enter_website(request):
    if request.session.get("checked"):
        return redirect("index")
    else:
        if request.method == "GET":
            enter_form = EnterForm(request)
            return render(request, "front/enter_website.html", locals())
        elif request.method == "POST":
            enter_form = EnterForm(request, request.POST)
            if enter_form.is_valid():
                request.session["checked"] = True
                return redirect("before_login")
            else:
                error = enter_form.errors
                return render(
                    request, 'front/enter_website.html',
                    {'enter_form': enter_form, 'error': error}
                )
