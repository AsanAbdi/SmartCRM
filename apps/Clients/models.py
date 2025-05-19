from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from datetime import date, datetime
from pydantic import EmailStr
from enum import Enum

from config.utils import utcnow_time
from apps.Users.models import User


class ClientSource(str, Enum):
    website = "website"
    instagram = "instagram"
    whatsapp = "whatsapp"
    telegram = "telegram"
    facebook = "facebook"
    referral = "referral"
    offline = "offline"
    other = "other"


class ClientSegment(str, Enum):
    retail = "retail"
    wholesale = "wholesale"
    vip = "vip"
    lead = "lead"
    prospect = "prospect"
    churned = "churned"
    partner = "partner"
    test = "test"


class ClientBase(SQLModel):
    full_name: Optional[str] = Field(max_length=255)
    email: Optional[EmailStr] = Field(max_length=255)
    phone_number: Optional[str] = Field(max_length=20, regex=r"^\+\d{7,19}$")
    source: Optional[ClientSource]
    segment: Optional[ClientSegment]
    assigned_to: Optional[UUID]
    location: Optional[str] = Field(max_length=255)
    birth_date: Optional[date]
    notes: Optional[str] = Field(max_length=10000)


class ClientCreate(ClientBase):
    full_name: str
    email: EmailStr
    phone_number: str
    source: ClientSource
    segment: ClientSegment


class ClientUpdate(ClientBase):
    is_active: Optional[bool]
    updated_at: Optional[datetime]


class ClientPublic(SQLModel):
    id: UUID
    full_name: str
    created_at: datetime
    email: EmailStr
    phone_number: str
    source: ClientSource
    segment: ClientSegment
    location: Optional[str]
    birth_date: Optional[date]
    notes: Optional[str]
    
    class Config:
        orm_mode = True



class ClientListItem(SQLModel):
    id: UUID
    full_name: str
    email: EmailStr
    phone_number: str
    source: ClientSource
    segment: ClientSegment
    
    class Config:
        orm_mode = True


class ClientList(SQLModel):
    items: list[ClientListItem]
    total_count: int
    
    class Config:
        orm_mode = True


class Client(SQLModel, table=True):
    __tablename__ = "client"

    id: UUID = Field(default_factory=uuid4, primary_key=True, unique=True, index=True)
    full_name: str = Field(max_length=255, index=True)
    email: EmailStr = Field(max_length=255, index=True, unique=True)
    phone_number: str = Field(max_length=20, unique=True, index=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utcnow_time)
    updated_at: datetime = Field(default_factory=utcnow_time)
    source: ClientSource = Field(index=True)
    segment: ClientSegment = Field(index=True)
    assigned_to: Optional[UUID] = Field(foreign_key="user.id")
    location: Optional[str] = Field(default=None, max_length=255)
    birth_date: Optional[date] = Field(default=None)
    notes: Optional[str] = Field(default=None, max_length=10000)
