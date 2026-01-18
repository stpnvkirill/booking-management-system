"""
DELETE /api/rooms/{id} - Удаление (деактивация) комнаты

Исполнитель: [ИМЯ]
"""
from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.security import security
from app.depends import AsyncSession, provider
from app.infrastructure.database.models.resources import Resource, ResourceType
from app.infrastructure.database.models.users import User

router = APIRouter()


@router.delete("/{room_id}", summary="Удаление комнаты")
async def delete_room(
    room_id: uuid.UUID,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """
    Мягкое удаление комнаты (is_active = False).
    
    Логика:
    1. Найти комнату по ID
    2. Проверить права доступа
    3. Установить is_active = False
    4. Вернуть {"ok": True}
    """
    # TODO: Реализовать мягкое удаление комнаты
    raise HTTPException(status_code=501, detail="Not implemented")
