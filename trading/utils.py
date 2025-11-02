from django.contrib.auth import get_user_model
from rest_framework.request import Request

User = get_user_model()

def require_user_key(request: Request):
    """
    Validate headers: X-USER-KEY (user.secret_key) and user_email in body or query.
    Returns User instance or None.
    """
    xkey = request.headers.get('X-USER-KEY') or request.META.get('HTTP_X_USER_KEY')
    user_email = request.data.get('user_email') or request.query_params.get('user_email') or request.headers.get('X-USER-EMAIL')
    if not xkey or not user_email:
        return None
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        return None
    if user.secret_key != xkey:
        return None
    return user



import os
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings

# We require settings.FERNET_KEY to be set from environment.
def _get_fernet():
    key = getattr(settings, 'FERNET_KEY', None)
    if not key:
        raise RuntimeError("FERNET_KEY is not configured in Django settings")
    if isinstance(key, str):
        key = key.encode()
    return Fernet(key)

def encrypt_text(plaintext: str) -> str:
    """
    Encrypts plaintext and returns a url-safe base64 token string.
    """
    if plaintext is None:
        return ''
    f = _get_fernet()
    token = f.encrypt(plaintext.encode())
    return token.decode()

def decrypt_text(token: str) -> str:
    """
    Decrypts token produced by encrypt_text.
    """
    if not token:
        return ''
    f = _get_fernet()
    try:
        data = f.decrypt(token.encode())
    except InvalidToken:
        raise RuntimeError("Invalid encryption token or wrong FERNET_KEY")
    return data.decode()

