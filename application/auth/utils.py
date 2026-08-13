from datetime import timedelta, datetime, timezone

import jwt
from core.config import settings
import bcrypt

def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expires_min,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm
    )
    return encoded

def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm
):
    decoded = jwt.decode(
        key=token,
        public_key=public_key,
        algorithms=algorithm
    )
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)

def check_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


def create_tokens(user_id: int, email: str):
    access_payload = {
        'sub': str(user_id),
        'email': email,
        'type': 'access'
    }
    access_jwt = encode_jwt(
        payload=access_payload,
        expire_timedelta=timedelta(minutes=settings.auth_jwt.access_token_expires_min),
    )

    refresh_payload = {
        'sub': str(user_id),
        'type': 'refresh'
    }

    refresh_jwt = encode_jwt(
        payload=refresh_payload,
        expire_timedelta=timedelta(days=30)
    )

    return access_jwt, refresh_jwt

