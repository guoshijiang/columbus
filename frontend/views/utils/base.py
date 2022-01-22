# encoding=utf-8

import time
from decimal import Decimal

from common.helpers import d0


def keep_two(value):
    if value in ["", None, "None", 0, d0]:
        return "0"
    dec_value = Decimal(value).quantize(Decimal("0.00"))
    return (
        dec_value.to_integral()
        if dec_value == dec_value.to_integral()
        else dec_value.normalize()
    )


def keep_four(value):
    if value in ["", None, "None", 0, d0]:
        return "0"
    dec_value = Decimal(value).quantize(Decimal("0.0000"))
    return (
        dec_value.to_integral()
        if dec_value == dec_value.to_integral()
        else dec_value.normalize()
    )
