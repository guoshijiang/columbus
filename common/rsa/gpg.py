import string
import random
import gnupg


gpg = gnupg.GPG("gpg")


class GPGKeygen:
    key_type: str = "RSA"
    key_length: int = 1024
    name_email: str = "backend@163.com"
    passphrase: str = "1234567890"

    def __init__(self,  key_type: str = "RSA", key_length: int = 2048,
            name_email: str="backend@163.com", passphrase:str="1234567890"):
        self.key_type = key_type
        self.key_length = key_length
        self.name_email = name_email
        self.passphrase = passphrase

    def create_gpg_key(self):
        input_data = gpg.gen_key_input(
            key_type=self.key_type,
            key_length=self.key_length,
            name_email=self.name_email,
            passphrase=self.passphrase
        )
        key = gpg.gen_key(input_data)
        public_keys = gpg.export_keys(key)
        private_key = gpg.export_keys(key, True, True)
        with open('./keyfile.asc', 'w') as f:
            f.write(public_keys)
            f.write(private_key)
        return public_keys, private_key

    def import_key(self, key_file):
        key_data = open(key_file).read()
        result = gpg.import_keys(key_data)
        return result

    def list_keys(self):
        public_keys = gpg.list_keys()
        private_keys = gpg.list_keys(True)
        return public_keys, private_keys

    def encrypt(self, unencrypted_data: str, email: str):
        encrypted = gpg.encrypt(unencrypted_data, email)
        print("encrypted =", encrypted.ok)
        print("encrypted_data.stderr = ", encrypted.stderr)
        encrypted_string = str(encrypted)
        return encrypted_string

    def decrypt(self, ncrypted_data: str, passphrase: str):
        decrypted_data = gpg.decrypt(ncrypted_data, passphrase=passphrase)
        return decrypted_data

