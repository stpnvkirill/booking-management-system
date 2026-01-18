"""
Pydantic схемы для работы с комнатами (переговорными).
"""
from typing import Optional, Any
import uuid
from pydantic import BaseModel, Field


class RoomBase(BaseModel):
    """Базовая схема комнаты."""
    name: str = Field(..., min_length=1, max_length=100, description="Название комнаты")
    description: Optional[str] = Field(None, description="Описание комнаты")
    capacity: int = Field(..., ge=1, description="Вместимость комнаты")


class RoomCreate(RoomBase):
    """Схема для создания комнаты (POST /api/rooms)."""
    pass


class RoomUpdate(BaseModel):
    """Схема для обновления комнаты (PUT /api/rooms/{id})."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None)
    capacity: Optional[int] = Field(None, ge=1)


class RoomResponse(RoomBase):
    """Схема ответа с данными комнаты."""
    id: uuid.UUID
    customer_id: uuid.UUID
    is_active: bool
    created_at: Any
    updated_at: Any

    class Config:
        from_attributes = True
