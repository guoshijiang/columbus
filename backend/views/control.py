# encoding=utf-8
import logging

import pytz
import time
from django.db import transaction
from django.conf import settings
from django.db.models import F, Q
from django.shortcuts import redirect, render, reverse


def bar_index(request):
    return redirect("b_index")


def bar_marchant(request):
    return redirect("b_marchants_list")


def bar_goods(request):
    return redirect("b_goods_list")


def bar_order(request):
    return redirect("b_order_list")

def bar_user(request):
    return redirect("user_list")


def bar_wallet(request):
    return redirect("coin_list")
    

def bar_forum(request):
    return redirect("b_forum_cat")


def bar_help(request):
    return redirect("bnews_list")

