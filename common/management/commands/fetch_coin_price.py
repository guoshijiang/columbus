# encoding=utf-8

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from common.models import Asset
from common.helpers import dec
from common.http_client import RestClient

BaseUrl = "https://dncapi.bqiapp.com/api/coin/web-coinrank?page=1&type=-1&pagesize=%s&webp=1"


class Command(BaseCommand):
    def handle(self, *args, **options):
        request_url = BaseUrl
        rc = RestClient(request_url)
        params = {
        }
        result = rc.api_get(api_url="", params=params)
        data_list = result.get("data", None)
        if data_list is not None:
            for data in data_list:
                if data['name'] == "ETH":
                    Asset.objects.filter(name='ETH').update(
                        usd_price=dec(data['current_price_usd']),
                        cny_price=dec(data['current_price']),
                    )
                elif data['name'] == "USDT":
                    Asset.objects.filter(name='USDT').update(
                        usd_price=dec(data['current_price_usd']),
                        cny_price=dec(data['current_price']),
                    )
                else:
                    continue



