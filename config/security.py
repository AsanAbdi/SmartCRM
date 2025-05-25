from passlib.context import CryptContext
from typing import Any
import jwt
from datetime import timedelta, datetime
from sqlmodel import Session

from config.settings import settings
from apps.Login.models import TokenData, TokenType


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_token(subject: str | Any, expires_delta: timedelta) -> Any:
    expire = datetime.now() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_token(
    token: str,
) -> TokenData | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, ALGORITHM)
        sub = payload.get("sub")
        if sub is None:
            return None
        
        return TokenData(username=sub)
    except jwt.PyJWTError:
        return None
