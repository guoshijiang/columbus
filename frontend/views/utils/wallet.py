# encoding=utf-8

import json
import logging

import requests
from django.conf import settings

from common.http_client import RestClient


# 获取钱包地址
def create_wallet(user_id: str, wallet_id: int = 1):
    api_url = settings.WALLET_URL + "wallet/create_address"
    params = {"user_id": user_id, "wallet_id": wallet_id}
    resp = requests.post(api_url, data=params)
    if resp.status_code == 200:
        content = resp.content.decode("utf-8")
        resp_json = json.loads(content)
        return resp_json
    else:
        return None


# 获取钱包通知信息
def sync_tx():
    pass


# 提交交易到钱包
def submit_tx():
    pass
