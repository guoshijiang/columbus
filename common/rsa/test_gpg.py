# encoding=utf-8
import gnupg
import io

gpg = gnupg.GPG('gpg')


# input_data = gpg.gen_key_input(
#     key_type="RSA",
#     key_length=2048,
#     name_email="backend@163.com",
#     passphrase="12345678"
# )
# key = gpg.gen_key(input_data)
# print(key.fingerprint)
#
# ascii_armored_public_keys = gpg.export_keys(key)
# ascii_armored_private_keys = gpg.export_keys(key, True, True)
# with open('./keyfile.asc', 'w') as f:
#     f.write(ascii_armored_public_keys)
#     f.write(ascii_armored_private_keys)
# ret = gpg.import_keys("./keyfile.asc")

key_data = open("./0x584FBDF7_public.asc").read()
key = gpg.import_keys(key_data)
print(key.fingerprints)

unencrypted_string = "123456"
encrypted = gpg.encrypt(unencrypted_string, key.fingerprints[0])
# print(encrypted.stderr)
print("encrypted_string = ", str(encrypted))
