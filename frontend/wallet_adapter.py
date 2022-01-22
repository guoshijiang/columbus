# encoding=utf-8

import json
from django.conf import settings
from common.http_client import RestClient
from common.helpers import dec, d0


WalletUuid = "ColumbusWallet%000001%V101"


# 生成钱包地址
def create_address(user_id: int):
    api_path = 'wallet/create_address'
    rest_client = RestClient(settings.WALLET_URL)
    data = {
        "user_id": str(user_id),
        "wallet_id": WalletUuid
    }
    resp = rest_client.api_post(
        api_url=api_path,
        data=json.dumps(data)
    )
    if resp['status'] is True:
        return resp['data']
    else:
        raise Exception("Get Address Fail")


# 提交提现信息
def submit_withdraw(
        user_id: int, asset_name: str, chain_name: str, withdraw_id: int,
        from_addr:str, to_address: str, amount: dec) -> bool:
    api_path = 'wallet/withdraw'
    rest_client = RestClient(settings.WALLET_URL)
    data = {
        "asset_name": asset_name,
        "chain_name": chain_name,
        "user_uuid": str(user_id),
        "withdraw_id": withdraw_id,
        "from_addr": from_addr,
        "to_addr": to_address,
        "amount": amount,
        "trans_fee": d0
    }
    resp = rest_client.api_post(
        api_url=api_path,
        data=json.dumps(data)
    )
    if resp['status'] is True:
        return True
    else:
        return False
