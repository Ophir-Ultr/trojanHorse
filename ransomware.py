import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

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


def encrypt_file(input_file_path, key):
    plaintext = read_file(input_file_path)
    encrypted_data = encrypt_data(plaintext.decode(), key)
    write_file(input_file_path, encrypted_data)


def decrypt_file(input_file_path, key):
    ciphertext = read_file(input_file_path)
    decrypted_data = decrypt_data(ciphertext, key)
    write_file(input_file_path, decrypted_data.encode())

def read_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

def write_file(file_path, data):
    with open(file_path, 'wb') as f:
        f.write(data)



if __name__ == "__main__":
    # encrypted_data = encrypt_data("Hello World", "kuskus")
    # print("encrypted data:", encrypted_data)
    # decrypt_data(encrypted_data, "kuskus")
    encrypted_file_path = "C:\\Users\\danie\\OneDrive\\Documents\\scripts\\gama\\gama\\testtext2.txt"
    # encrypt_file(encrypted_file_path, "kuskus")
    decrypt_file(encrypted_file_path, "kuskus")