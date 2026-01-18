"""
PUT /api/rooms/{id} - Обновление данных о комнате

Исполнитель: [ИМЯ]
"""
from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.security import security
from app.depends import AsyncSession, provider
from app.infrastructure.database.models.resources import Resource, ResourceType
from app.infrastructure.database.models.users import User
from .schema import RoomUpdate, RoomResponse

router = APIRouter()


@router.put("/{room_id}", response_model=RoomResponse, summary="Обновление данных о комнате")
async def update_room(
    room_id: uuid.UUID,
    room_in: RoomUpdate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """
    Обновление данных переговорной комнаты.
    
    Логика:
    1. Найти комнату по ID
    2. Проверить права доступа
    3. Обновить поля из room_in
    4. Вернуть обновлённую комнату
    """
    # TODO: Реализовать обновление комнаты
    raise HTTPException(status_code=501, detail="Not implemented")
