from collections.abc import Generator
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlmodel import Session

from config.settings import settings
from config.db import engine


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]