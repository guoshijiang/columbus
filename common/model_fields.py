import json

from django.db import models


class DecField(models.DecimalField):
    def __init__(self, **kw):
        kw.setdefault("max_digits", 65)
        kw.setdefault("decimal_places", 30)
        super(DecField, self).__init__(**kw)


class IdField(models.CharField):
    def __init__(self, **kwargs):
        kwargs.setdefault("max_length", 100)
        super(IdField, self).__init__(**kwargs)
