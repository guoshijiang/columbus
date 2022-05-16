from secp256k1 import PrivateKey
from pycoin.encoding.b58 import a2b_hashed_base58, b2a_hashed_base58
from pycoin.encoding.hexbytes import h2b, b2h
from pybitcoin.deterministic import encode_pubkey
from tronapi import Tron


def base58_to_hex(address_base58: str) -> str:
    return a2b_hashed_base58(address_base58).hex()


def hex_to_base58(address_hex):
    return b2a_hashed_base58(h2b(address_hex))


def pubkey_to_address(pubkey):
    pubkey = encode_pubkey(pubkey, 'bin')
    pubkey = pubkey[1:]
    pubkey_hash = Tron.keccak(pubkey)
    addr = "41" + b2h(pubkey_hash[12:])
    return hex_to_base58(addr)


def privkey_to_pubkey(privkey: str) -> str:
    privkey_obj = PrivateKey(bytes.fromhex(privkey))
    return privkey_obj.pubkey.serialize().hex()


def create_address():
    privkey = PrivateKey().serialize()
    public_key = privkey_to_pubkey(privkey)
    return {
        "privkey": privkey,
        "public_key": public_key,
        "address": pubkey_to_address(public_key)
    }
