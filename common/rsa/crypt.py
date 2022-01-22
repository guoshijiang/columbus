import rsa


def rsa_generate_key(bytes: int):
    f, e = rsa.newkeys(bytes)
    e = e.save_pkcs1()
    with open("private.pem", "wb") as x:
        x.write(e)
    f = f.save_pkcs1()
    with open("public.pem", "wb") as x:
        x.write(f)
    return f, e


def rsa_encrypt(content: str, public: str):
    public_key = rsa.PublicKey.load_pkcs1(public)
    cipher_text = rsa.encrypt(content, public_key)
    return cipher_text


def rsa_decrypt(cipher_text, private_key):
    text = rsa.decrypt(cipher_text, private_key)
    return text
