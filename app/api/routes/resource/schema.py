from typing import Optional, Any
import uuid
from pydantic import BaseModel, Field
from app.infrastructure.database.models.resources import ResourceType


class ResourceBase(BaseModel):
    type: ResourceType = Field(..., description="Тип ресурса: meeting_room, specialist, equipment")
    name: str = Field(..., min_length=1, max_length=100, description="Название ресурса или ФИО специалиста")
    description: Optional[str] = Field(None, description="Описание ресурса")
    
    # Optional specific fields
    capacity: Optional[int] = Field(None, ge=1, description="Вместимость (только для переговорных)")
    position: Optional[str] = Field(None, description="Должность (только для специалистов)")
    schedule: Optional[dict[str, Any]] = Field(None, description="График работы (только для специалистов)")


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None)
    capacity: Optional[int] = Field(None, ge=1)
    position: Optional[str] = Field(None)
    schedule: Optional[dict[str, Any]] = Field(None)
    # Type usually shouldn't change, but depends on logic. Keeping it immutable for now or explicit.


class ResourceModel(ResourceBase):
    id: uuid.UUID
    customer_id: uuid.UUID
    is_active: bool
    created_at: Any # Using Any to avoid datetime import issues in schema if not strictly needed, or import datetime
    updated_at: Any

    class Config:
        from_attributes = True
