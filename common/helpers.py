import hashlib
import json
import logging
import time
from datetime import date, datetime, timedelta
from decimal import ROUND_UP
from decimal import Context as DecimalContext
from decimal import Decimal, InvalidOperation
from typing import Any, Dict
from urllib.parse import urlencode

import pytz
import requests
from dateutil import parser
from django.conf import settings
from django.core.paginator import EmptyPage
from django.http import HttpRequest, JsonResponse
from django.utils.timezone import localtime, now

from common.paginator import MyPaginator


def make_timestamp() -> float:
    return time.time() * 1000


def ok_json(data: Any) -> JsonResponse:
    return JsonResponse({"ok": True, "code": 200, "result": data})


def error_json(msg: str, code: int = -1, status: int = 200) -> JsonResponse:
    return JsonResponse({"ok": False, "code": code, "msg": msg}, status=status)


def floor_decimal(amount: Decimal, digits: int = 18) -> Decimal:
    return amount.quantize(
        Decimal("1E-%d" % digits), context=DecimalContext(rounding=ROUND_UP)
    )


def parse_decimal(value: Any, default: Any = "0", digits: int = 18) -> Decimal:
    try:
        # if isinstance(value, float):
        #    value = str(value)
        return floor_decimal(Decimal(value), digits=digits)
    except (InvalidOperation, TypeError):
        return Decimal(default)


dec = parse_decimal
d0 = dec("0")
d1 = dec("1")


def _xx_decprice(value: Any) -> Decimal:
    return dec(value, digits=6)


decprice = dec


def decstr(value: Decimal) -> str:
    return "{:f}".format(value)


def build_sign(params: Dict[str, Any], secretKey: str) -> str:
    data = sorted(params.items()) + [("secret_key", secretKey)]
    encoded = urlencode(data)
    return hashlib.md5(encoded.encode("utf8")).hexdigest().upper()


MIN = dec("0", digits=8)


def parse_int(v, default=0):
    try:
        v = int(v)
    except (ValueError, TypeError) as e:
        v = default
    return v


def get_page(request: HttpRequest) -> int:
    page = parse_int(request.GET.get("page", 1), 1)
    if page < 1:
        page = 1
    return page


PAGE_SIZE = 10


def paged_items(
    request: HttpRequest, qs, pagesize=PAGE_SIZE, page_cls=MyPaginator
):
    paginator = page_cls(qs, pagesize, adjacent_pages=3)
    page = get_page(request)
    try:
        items = paginator.page(page)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    args = {}
    for key, value in request.GET.items():
        if key != "page":
            args[key] = value.encode("utf-8")
    if len(args) == 0:
        items.prefix_uri = request.path + "?"
    else:
        items.prefix_uri = request.path + "?" + urlencode(args) + "&"
    return items


def sleep(sleep_time: float) -> None:
    time.sleep(sleep_time)


def vformat(value: Decimal, digits: int = 8) -> str:
    fmt = "%%i.%%0%di" % digits
    k = pow(10, digits)

    sign = ""
    if value < 0:
        value = -value
        sign = "-"

    upv = value * k

    r = fmt % (upv // k, upv % k)
    r = sign + r.rstrip("0").rstrip(".")
    if r == "-0":
        r = "0"
    return r


def utc_now() -> datetime:
    return now()


def current_now() -> datetime:
    return localtime(utc_now())


def str2current_time(select_time, default) -> datetime:
    try:
        return normalize_datetime(parser.parse(select_time))
    except:
        return default


def normalize_datetime(value, tz_name=settings.TIME_ZONE):
    tz = pytz.timezone(tz_name)
    return value.astimezone(tz)


def date_to_str(date_time: date, time_format: str = "%Y-%m-%d") -> str:
    return date_time.strftime(time_format)


def utc2str(d: datetime, format_str: str = "%Y%m%d%H%M%S") -> str:
    return d.strftime(format_str)


class JsonEncoder(json.JSONEncoder):
    def object_to_json(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding="utf-8")
        return json.JSONEncoder.default(self, obj)
