from collections.abc import Generator
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import jwt
from sqlmodel import Session

from config.settings import settings
from apps.Users.models import User
from config.security import ALGORITHM
from config.db import engine


scheme_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)



def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]

def get_current_user(
    session: SessionDep,
    token: str = Depends(scheme_oauth2)
) -> User:
    exception = HTTPException(
        detail="Invalid token provided",
        status_code=status.HTTP_400_BAD_REQUEST
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, ALGORITHM)
        user_id = payload.get("sub")
        if not user_id:
            raise exception
    except jwt.PyJWTError:
        raise exception
    
    user = session.get(User, user_id)
    if not user or not user.is_active:
        raise exception
    return user