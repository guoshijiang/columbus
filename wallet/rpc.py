from .address import base58_to_hex


async def get_account_balance(self, address):
    path = "/walletsolidity/getaccount"
    payload = {'address': base58_to_hex(address)}
    data = await self.post(path, payload=payload)
    return data.get('balance', 0) if data and isinstance(data, dict) else None