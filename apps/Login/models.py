from sqlmodel import SQLModel
from enum import Enum


class TokenType(str, Enum):
    refresh_token = "refresh_token"
    access_token = "access_token"
    

class Token(SQLModel):
    access_token: str
    token_type: str
    sub: str
    

class TokenData(SQLModel):
    username: str