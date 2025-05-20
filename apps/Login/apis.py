from sqlalchemy import JSON
from sqlmodel import select
from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi.responses import JSONResponse

from apps.Login.models import Token
from apps.deps import SessionDep
from apps.Users.models import User
from config.settings import settings
from config.security import verify_password, create_access_token


router = APIRouter(prefix="/login", tags=["login"])


@router.post("/access-token", response_model=Token)
def create_token(
    session: SessionDep, 
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    db_user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not db_user:
        raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
    if not db_user.is_active:
        raise HTTPException(detail="Inactive User", status_code=status.HTTP_400_BAD_REQUEST)
    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(detail="Wrong data", status_code=status.HTTP_400_BAD_REQUEST)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(
            db_user.id, expires_delta=access_token_expires
        ),
        token_type="bearer",
        sub=str(db_user.id)
    )
