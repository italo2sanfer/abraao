import time

import jwt
from django.conf import settings
from django.core.cache import cache

SECRET_KEY = getattr(settings, "SECRET_KEY", "default-secret")
CACHE_KEY_LAST_TOKEN = "last_temp_token"


def generate_temp_token():
    """
    Gera um token temporário que expira em 5 minutos.
    """
    payload = {
        "exp": int(time.time()) + int(settings.TOKEN_EXPIRY),
        "iat": int(time.time()),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    # Armazenar no cache para verificação rápida
    cache.set(f"temp_token_{token}", True, timeout=int(settings.TOKEN_EXPIRY))
    # Armazenar o último token gerado
    cache.set(CACHE_KEY_LAST_TOKEN, token, timeout=int(settings.TOKEN_EXPIRY))
    return token


def is_token_valid(token):
    """
    Verifica se o token é válido e não expirou.
    """
    try:
        # Verificar no cache primeiro
        if not cache.get(f"temp_token_{token}"):
            return False
        # Decodificar para verificar expiração
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True
    except jwt.ExpiredSignatureError:
        cache.delete(f"temp_token_{token}")
        return False
    except jwt.InvalidTokenError:
        return False


def get_valid_token():
    """
    Retorna um token válido. Se o último gerado ainda for válido, retorna ele; senão, gera um novo.
    """
    last_token = cache.get(CACHE_KEY_LAST_TOKEN)
    if last_token and is_token_valid(last_token):
        return last_token
    else:
        return None


def get_token_remaining_time(token):
    """
    Retorna o tempo restante de um token em segundos.
    Retorna um dicionário com 'remaining_time' (int) ou 'error' (str).
    """
    try:
        # Decodificar o token sem validar expiração para obter o payload
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False}
        )
        exp_timestamp = payload.get("exp")

        if not exp_timestamp:
            return {"error": "Token sem data de expiração"}

        current_time = int(time.time())
        remaining_time = exp_timestamp - current_time

        # Se o tempo é negativo, o token já está expirado
        if remaining_time < 0:
            return {"error": "Token expirado", "remaining_time": 0}

        return {"remaining_time": remaining_time}
    except jwt.InvalidTokenError as e:
        return {"error": f"Token inválido: {str(e)}"}
