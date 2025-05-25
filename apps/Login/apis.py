from sqlmodel import select
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from apps.Login.models import Token, TokenType
from apps.deps import SessionDep
from apps.Users.models import User
from config.settings import settings
from config.security import verify_password, create_token, verify_token


router = APIRouter(prefix="/login", tags=["login"])


@router.post("/access-token", response_model=Token)
def create_access_token(
    session: SessionDep, 
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response
) -> Token:
    db_user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not db_user:
        raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
    if not db_user.is_active:
        raise HTTPException(detail="Inactive User", status_code=status.HTTP_400_BAD_REQUEST)
    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(detail="Wrong data", status_code=status.HTTP_400_BAD_REQUEST)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    max_hours = int((settings.REFRESH_TOKEN_EXPIRE_MINUTES // 60) * 3)
    refresh_token_expire = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_token(subject=db_user.username, expires_delta=refresh_token_expire)
    response.set_cookie(
        key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite="Lax", max_age=max_hours
    )
    return Token(
        access_token=create_token(
            db_user.username, expires_delta=access_token_expires
        ),
        token_type="Bearer",
        sub=str(db_user.username)
    )


@router.post("/refresh-token", response_model=Token)
def create_refresh_token(
    db: SessionDep,
    request: Request
) -> Token:
    refresh_token = request.cookies.get("refresh_token", None)
    if refresh_token is None:
        raise HTTPException(detail="Refresh token is not provided", status_code=status.HTTP_400_BAD_REQUEST)
    user_data = verify_token(refresh_token)
    if not user_data:
        raise HTTPException(detail="Invalid refresh token", status_code=status.HTTP_400_BAD_REQUEST)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_token(
            user_data.username, expires_delta=refresh_token_expires
        ),
        token_type="Bearer",
        sub=str(user_data.username)
    )
