from enum import Enum
from typing import Optional
from pydantic import field_validator
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime
from config.utils import utcnow_time
from uuid import UUID, uuid4
import json
from typing import Any
from datetime import datetime, timezone


class InteractionType(str, Enum):
    call = "call"
    meeting = "meeting"
    email = "email"
    chat = "chat"
    service = "service"
    subscription = "subscription"

class InteractionStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"

class ChannelType(str, Enum):
    phone = "phone"
    telegram = "telegram"
    whatsapp = "whatsapp"
    instagram = "instagram"


class InteractionCreate(SQLModel):
    client_id: UUID
    user_id: UUID
    interaction_type: InteractionType
    interaction_datetime: datetime
    channel: ChannelType
    interaction_status: InteractionStatus
    revenue: Optional[float]
    cost_center: Optional[str] = Field(max_length=255)
    notes: Optional[str] = Field(max_length=10000)
    external_id: Optional[str]


class InteractionUpdate(SQLModel):
    is_active: Optional[bool]
    client_id: Optional[UUID]
    user_id: Optional[UUID]
    interaction_type: Optional[InteractionType]
    channel: Optional[ChannelType]
    interaction_status: Optional[InteractionStatus]
    interaction_datetime: Optional[datetime]
    revenue: Optional[float]
    cost_center: Optional[str]
    notes: Optional[str] = Field(max_length=10000)
    external_id: Optional[str]

    class Config:
        orm_mode = True


class InteractionPublic(SQLModel):
    id: UUID
    client_id: UUID
    user_id: UUID
    is_active: bool
    interaction_type: InteractionType
    interaction_status: InteractionStatus
    interaction_datetime: datetime
    channel: ChannelType
    revenue: Optional[float]
    cost_center: Optional[str]
    notes: Optional[str]
    external_id: Optional[str]
    
    class Config:
        orm_mode = True


class InteractionListItem(SQLModel):
    id: UUID
    client_id: UUID
    user_id: UUID
    interaction_type: InteractionType
    interaction_status: InteractionStatus
    interaction_datetime: datetime


class InteractionList(SQLModel):
    items: list[InteractionListItem]
    total_count: int
    
    class Config:
        orm_mode = True


class Interaction(SQLModel, table=True):
    __tablename__ = "interaction"
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, unique=True)
    created_at: datetime = Field(sa_column=Column(DateTime, default=utcnow_time))
    updated_at: datetime = Field(sa_column=Column(DateTime, default=utcnow_time, onupdate=utcnow_time))
    is_active: bool = Field(default=True)
    client_id: UUID = Field(foreign_key="client.id", index=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    interaction_type: InteractionType = Field(default=InteractionType.chat)
    interaction_datetime: datetime = Field(index=True)
    channel: ChannelType = Field(default=ChannelType.phone)
    interaction_status: InteractionStatus = Field(default=InteractionStatus.pending, index=True)
    revenue: Optional[float]
    cost_center: Optional[str] = Field(max_length=255)
    notes: Optional[str] = Field(max_length=10000)
    external_id: Optional[str]
    engagement_score: Optional[float]
    churn_probability: Optional[float]
    predicted_ltv: Optional[float]

    class Config:
        orm_mode = True