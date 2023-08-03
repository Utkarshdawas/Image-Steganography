from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import binascii

def encrypt_text(key, text):
    backend = default_backend()
    cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.TripleDES.block_size).padder()

    padded_text = padder.update(text.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded_text) + encryptor.finalize()
    return binascii.hexlify(ciphertext).decode()

def decrypt_text(key, ciphertext):
    backend = default_backend()
    cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(algorithms.TripleDES.block_size).unpadder()

    ciphertext = binascii.unhexlify(ciphertext)
    decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()
    unpadded_text = unpadder.update(decrypted_text) + unpadder.finalize()
    return unpadded_text.decode()

# Example usage
key = input("Enter the key (24 bytes): ").encode()
text = 'Hello, World!'

encrypted_text = encrypt_text(key, text)
print("Encrypted text:", encrypted_text)

decrypted_text = decrypt_text(key, encrypted_text)
print("Decrypted text:", decrypted_text)
