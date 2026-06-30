import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import os

def pad(data: bytes, block_size: int = 16) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    if pad_len == 0: pad_len = block_size
    return data + bytes([pad_len]) * pad_len

def unpad(padded: bytes, block_size: int = 16) -> bytes:
    pad_len = padded[-1]
    if pad_len < 1 or pad_len > block_size:
        raise ValueError("bad padding")
    if padded[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("bad padding")
    return padded[:-pad_len]    


def encrypt_data(plaintext, key):
        key = hashlib.sha256(key.encode()).digest()  # Derive a 256-bit key from the password

        iv = Random.new().read(AES.block_size) # Initialization vector
        cipher = AES.new(key, AES.MODE_CBC, iv)

        raw = pad(plaintext.encode()) 
        return iv + cipher.encrypt(raw)

def decrypt_data(ciphertext, key):
        key = hashlib.sha256(key.encode()).digest()  # Derive a 256-bit key from the password

        iv = ciphertext[:AES.block_size]
        data = ciphertext[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)

        plaintext = cipher.decrypt(data)
        plaintext = unpad(plaintext)
        return plaintext.decode()

 

def read_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

def write_file(file_path, data):
    with open(file_path, 'wb') as f:
        f.write(data)         


def encrypt_file(input_file_path, key):
    plaintext = read_file(input_file_path)
    encrypted_data = encrypt_data(plaintext.decode(), key)
    write_file(input_file_path, encrypted_data)


def decrypt_file(input_file_path, key):
    ciphertext = read_file(input_file_path)
    decrypted_data = decrypt_data(ciphertext, key)
    write_file(input_file_path, decrypted_data.encode())


def encrypt_directory(dirpath, key):
    for item in os.listdir(dirpath):
        fullpath = os.join(dirpath, item)
        if os.path.isdir(fullpath):
            encrypt_directory(fullpath)
        elif os.path.isfile(fullpath):
            encrypt_file(fullpath, key)
                 
def decrypt_directory(dirpath, key):
    for item in os.listdir(dirpath):
        fullpath = os.join(dirpath, item)
        if os.path.isdir(fullpath):
            decrypt_directory(fullpath)
        elif os.path.isfile(fullpath):
            decrypt_file(fullpath, key)
