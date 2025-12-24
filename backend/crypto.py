from Crypto.Cipher import AES
import os

def encrypt_file(file_path, key_path):
    with open(file_path, "rb") as f:
        data = f.read()
    with open(key_path, "rb") as kf:
        key = kf.read()
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    with open(file_path+".enc", "wb") as f:
        [f.write(x) for x in (cipher.nonce, tag, ciphertext)]
    os.remove(file_path)

def decrypt_file(enc_path, key_path):
    with open(enc_path, "rb") as f:
        nonce, tag, ciphertext = [f.read(x) for x in (16, 16, os.path.getsize(enc_path)-32)]
    with open(key_path, "rb") as kf:
        key = kf.read()
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    orig_path = enc_path.replace(".enc","")
    with open(orig_path, "wb") as f:
        f.write(data)
