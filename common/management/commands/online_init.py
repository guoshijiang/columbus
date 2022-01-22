# encoding=utf-8

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from common.models import Asset


class Command(BaseCommand):
    def handle(self, *args, **options):
        support_asset_list = settings.SUPPOR_ASSET
        for support_asset in support_asset_list:
            Asset.objects.create(
                name=support_asset["name"], chain_name=support_asset["chain_name"]
            )
