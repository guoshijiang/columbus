# encoding=utf-8


from django.core.management.base import BaseCommand
from common.models import Asset
from marchant.models import MarchantConfig


class Command(BaseCommand):
    def handle(self, *args, **options):
        mct_config = MarchantConfig.objects.filter(is_active=True).order_by("-id").first()
        usdt_amount = mct_config.usdt_amount
        eth_asset = Asset.objects.filter(name="ETH").first()
        eth_cprice = usdt_amount / eth_asset.usd_price
        mct_config.eth_amount = eth_cprice
        mct_config.save()
