import base64
import hashlib

from cryptography.fernet import Fernet


def encrypt_password(code: str, password: str):
    hash_bytes = hashlib.sha256(code.encode()).digest()
    key = base64.urlsafe_b64encode(hash_bytes)
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(password.encode()).decode()
    return encrypted_password


def decrypt_password(code: str, encrypted_password: str):
    hash_bytes = hashlib.sha256(code.encode()).digest()
    key = base64.urlsafe_b64encode(hash_bytes)
    cipher = Fernet(key)
    decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
    return decrypted_password


def set_passwd(code: str, password: str):
    from .models import Judite

    judite = Judite.objects.get(code=code)
    judite.set_passwd(password)
