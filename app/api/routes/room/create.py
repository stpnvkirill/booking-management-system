"""
POST /api/rooms - Создание комнаты для брони

Исполнитель: [ИМЯ]
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.security import security
from app.depends import AsyncSession, provider
from app.infrastructure.database.models.resources import Resource, ResourceType
from app.infrastructure.database.models.users import User, Customer
from .schema import RoomCreate, RoomResponse

router = APIRouter()


@router.post("/", response_model=RoomResponse, summary="Создание комнаты для брони")
async def create_room(
    room_in: RoomCreate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """
    Создание новой переговорной комнаты.
    
    Логика:
    1. Получить customer_id текущего пользователя
    2. Создать ресурс с type=MEETING_ROOM
    3. Вернуть созданную комнату
    """
    # TODO: Реализовать создание комнаты
    raise HTTPException(status_code=501, detail="Not implemented")
