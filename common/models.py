import uuid

from django.db import models

BoolYesOrNoSelect = [
    (x, x) for x in ["Yes", "No"]
]
PayWaySelect = [
    (x, x) for x in ["All", "ETH", "USDT"]
]
AdminOrUser = [
    (x, x) for x in ["Admin", "User"]
]


class BaseModel(models.Model):
    uuid = models.CharField(
        max_length=100,
        blank=True,
        unique=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True
    )
    updated_at = models.DateTimeField(
        auto_now=True, db_index=True
    )

    class Meta:
        abstract = True

    @property
    def UUID(self):
        return uuid.UUID(hex=self.uuid)

    def generate_uuid(self):
        self.uuid = uuid.uuid4().hex

    def save(self, *args, **kw):
        if not self.uuid:
            self.generate_uuid()
        return super(BaseModel, self).save(
            *args, **kw
        )


class DecField(models.DecimalField):
    def __init__(self, **kw):
        kw.setdefault("max_digits", 65)
        kw.setdefault("decimal_places", 30)
        super(DecField, self).__init__(**kw)


class IdField(models.CharField):
    def __init__(self, **kwargs):
        kwargs.setdefault("max_length", 100)
        super(IdField, self).__init__(**kwargs)


class Asset(BaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="资产名称",
    )
    chain_name = models.CharField(
        max_length=100, verbose_name="链名称"
    )
    usd_price = DecField(
        max_length=100, verbose_name="美元价格"
    )
    cny_price = DecField(
        max_length=100, verbose_name="人民币价格"
    )
    unit = models.CharField(
        max_length=100, verbose_name="币种精度"
    )
    is_active = models.BooleanField(
        default=True, verbose_name="是否是有效"
    )

    class Meta:
        verbose_name = "资产表"
        verbose_name_plural = "资产表"

    def __str__(self):
        return self.name

    def as_dict(self):
        return {"id": self.id}
