from Crypto.Cipher import AES
import os

KEY = b"1234567890abcdef1234567890abcdef"

def encrypt_file(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    cipher = AES.new(KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    with open(file_path + ".enc", "wb") as f:
        [f.write(x) for x in (cipher.nonce, tag, ciphertext)]
    os.remove(file_path)
