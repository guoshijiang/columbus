# encoding=utf-8
import base64
import hashlib
import binascii
import json
from django.shortcuts import redirect, render
from clbauth.models import UserWallet, WalletRecord, AuthUser, TansRecord
from common.models import Asset
from common.helpers import d0, dec, ok_json


def withdraw_deposit_notify(request):
    params = json.loads(request.body.decode())
    w_or_d = params.get('w_or_d')  # 0: 代表充值，1：代表提现
    user_uuid = params.get('user_uuid')
    print("user_uuid = ", user_uuid)
    asset_name = params.get('asset_name')
    chain_name = params.get('chain_name')
    from_address = params.get('from_address')
    print("from_address = ", from_address)
    to_address = params.get('to_address')
    amount = params.get('amount')
    tx_hash = params.get('tx_hash')
    tx_fee = params.get('tx_fee')
    withdraw_id = params.get('withdraw_id')
    status = params.get('status')  # 上报状态: 0:未发出; 1:已发出; 2:提现成功; 3:提现失败; 4:上报业务层成功 5:上报业务层失败
    user = AuthUser.objects.filter(id=int(user_uuid)).first()
    asset = Asset.objects.filter(name=asset_name, chain_name=chain_name).first()
    if w_or_d in ["0",  0]:        # 充值，直接提交记录，更新余额
        WalletRecord.objects.update_or_create(
            user=user,
            asset=asset,
            chain_name=chain_name,
            from_addr=from_address,
            to_addr=to_address,
            tx_hash=tx_hash,
            w_or_d='Deposit',
            amount=dec(amount),
            tx_fee=dec(tx_fee),
            status="Success"
        )
        TansRecord.objects.create(
            user=user,
            asset=asset,
            amount=dec(amount),
            trans_way="Input",
            source="钱包充值"
        )
        user_wallet = UserWallet.objects.filter(user=user).order_by("-id").first()
        if user_wallet is not None:
            user_wallet.balance += dec(amount)
            user_wallet.in_amount += dec(amount)
            user_wallet.save()
    else:
        wallet_record = WalletRecord.objects.filter(id=int(withdraw_id)).first()  # 更新提现状态
        wallet_record.status = status
        wallet_record.save()
        if status in ["3", 3]:  # 失败把用户的钱包退回钱包
            user_wallet = UserWallet.objects.filter(user=user).order_by("-id").first()
            if user_wallet is not None:
                user_wallet.balance += dec(amount)
                user_wallet.save()
        TansRecord.objects.create(
            user=user,
            asset=asset,
            amount=dec(amount),
            trans_way="Output",
            source="钱包提现"
        )
    return ok_json("success")
