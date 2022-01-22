# encoding=utf-8


from django.core.management.base import BaseCommand
from clbauth.models import WalletRecord
from frontend.wallet_adapter import submit_withdraw


class Command(BaseCommand):
    def handle(self, *args, **options):
        wallet_record_list = WalletRecord.objects.filter(w_or_d='Withdraw', status='Checked')
        for wallet_record in wallet_record_list:
            ok = submit_withdraw(
                user_id=wallet_record.user.id,
                asset_name=wallet_record.asset.name,
                chain_name=wallet_record.asset.chain_name,
                withdraw_id=wallet_record.id,
                from_addr=wallet_record.from_addr,
                to_address=wallet_record.to_addr,
                amount=wallet_record.amount,
            )
            if ok:
                print("submit withdraw suucee withdraw id is", wallet_record.id)
            else:
                print("submit withdraw fail withdraw id is", wallet_record.id)


