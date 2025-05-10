from typing import Literal, Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from datetime import date
from pydantic import EmailStr
from enum import Enum

from config.utils import utcnow_date


class UserRole(str, Enum):
    manager = "manager"
    admin = "admin"


class UserCore(SQLModel):
    username: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
    date_joined: date = Field(default_factory=utcnow_date)
    

class UserCreate(UserCore):
    password: str = Field(min_length=8, max_length=255)
    

class UserUpdate(SQLModel):
    username: Optional[str] = Field(max_length=255)
    email: Optional[EmailStr] = Field(max_length=255)
    is_active: Optional[bool]
    date_joined: Optional[date]


class UserPublic(SQLModel):
    id: UUID
    username: str
    email: EmailStr
    is_active: bool
    date_joined: date


class UserListItem(SQLModel):
    id: UUID
    username: str
    is_active: bool


class UserList(SQLModel):
    items: list[UserListItem]
    total_count: int


class User(SQLModel, table=True):
    __tablename__ = "user"
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, unique=True)
    username: str = Field(unique=True, index=True, max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = Field(default=True)
    date_joined: date = Field(default_factory=utcnow_date)
    hashed_password: str
    role: UserRole = Field(default=UserRole.manager)
