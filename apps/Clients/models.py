from typing import Literal, Optional
from uuid import UUID
from sqlmodel import SQLModel, Field
from datetime import date, datetime
from pydantic import EmailStr

from config.utils import utcnow



ClientSource = Literal[
    "website", "instagram", "whatsapp", "telegram", 
    "facebook", "referral", "offline", "other"
]
ClientSegment = Literal[
    "retail", "wholesale", "vip", "lead", 
    "prospect", "churned", "partner", "test"
]



class ClientBase(SQLModel):
    full_name: str = Field(max_length=255, index=True)
    email: EmailStr = Field(max_length=255, index=True, unique=True)
    phone_number: str = Field(max_length=20, unique=True, index=True)
    source: ClientSource = Field(max_length=10, index=True)
    segment: ClientSegment = Field(max_length=10, index=True)
    location: Optional[str] = Field(max_length=255)
    birth_date: Optional[date]
    notes: Optional[str]
    

class ClientCreate(ClientBase):
    pass


class ClientUpdate(SQLModel):
    full_name: Optional[str] = Field(default=None, max_length=255)
    email: Optional[EmailStr] = Field(default=None, max_length=255)
    phone_number: Optional[str] = Field(default=None, max_length=20)
    is_active: Optional[bool] = Field(default=True)
    source: Optional[ClientSource] = None
    segment: Optional[ClientSegment] = None
    location: Optional[str] = Field(default=None, max_length=255)
    birth_date: Optional[date] = None
    notes: Optional[str] = None
    assigned_to: Optional[str] = None

    
class ClientPublic(ClientBase):
    full_name: str
    email: EmailStr
    phone_number: str
    source: ClientSource
    segment: ClientSegment
    location: str
    birth_date: date
    notes: str


class ClientListRetrieve(ClientBase):
    full_name: str
    email: EmailStr
    phone_number: str
    source: ClientSource
    segment: ClientSegment
    
    
class ClientList(SQLModel):
    data: list[ClientListRetrieve]
    count: int


class Client(ClientBase, table=True):
    id: UUID = Field(primary_key=True, unique=True, index=True)
    full_name: str = Field(max_length=255, index=True)
    email: EmailStr = Field(max_length=255, index=True, unique=True)
    phone_number: str = Field(max_length=20, unique=True, index=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utcnow)
    source: str = Field(max_length=10, index=True)
    segment: str = Field(max_length=10, index=True)
    lifetime_value: Optional[float]
    last_activity_at: Optional[date]
    activity_count: Optional[int]
    prediction_score: Optional[float]
    assigned_to: Optional[str]
    location: Optional[str] = Field(max_length=255)
    birth_date: Optional[date]
    notes: Optional[str]
    
    
#Message
class Message(SQLModel):
    status: int
    message: str