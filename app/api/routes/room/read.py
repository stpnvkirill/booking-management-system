"""
GET /api/rooms/{id} - Получение данных о комнате

Исполнитель: [ИМЯ]
"""
from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.security import security
from app.depends import AsyncSession, provider
from app.infrastructure.database.models.resources import Resource, ResourceType
from app.infrastructure.database.models.users import User
from .schema import RoomResponse

router = APIRouter()


@router.get("/{room_id}", response_model=RoomResponse, summary="Получение данных о комнате")
async def get_room(
    room_id: uuid.UUID,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """
    Получение информации о конкретной комнате по ID.
    
    Логика:
    1. Найти ресурс по ID с type=MEETING_ROOM
    2. Проверить что is_active=True
    3. Вернуть данные комнаты
    """
    # TODO: Реализовать получение комнаты по ID
    raise HTTPException(status_code=501, detail="Not implemented")
