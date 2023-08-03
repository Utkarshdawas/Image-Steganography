from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import binascii

def encrypt_text(key, text):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()

    padded_text = padder.update(text.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded_text) + encryptor.finalize()
    return binascii.hexlify(ciphertext).decode()

def decrypt_text(key, ciphertext):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

    ciphertext = binascii.unhexlify(ciphertext)
    decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()
    unpadded_text = unpadder.update(decrypted_text) + unpadder.finalize()
    return unpadded_text.decode()