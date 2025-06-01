from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os
from dotenv import load_dotenv

load_dotenv()

def decrypt(user_key):
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=b'toomuchsalt97',
    iterations=100000,
    backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(user_key.encode()))
    f = Fernet(key)
    openai_key = os.getenv('OPENAI_KEY_ENC').encode()
    claude_key = os.getenv('CLAUDE_KEY_ENC').encode()
    openai_key_result = f.decrypt(openai_key).decode()
    claude_key_result = f.decrypt(claude_key).decode()
    return {'openai': openai_key_result, 'claude': claude_key_result}