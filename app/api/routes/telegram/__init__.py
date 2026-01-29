from typing import Annotated
from uuid import UUID

from aiogram import types
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.background import BackgroundTasks

from app.api.security import security
from app.bot import bot_manager
from app.config import config
from app.domain.services import user_service
from app.infrastructure.database import User

from .schema import AddBotModel

router = APIRouter(tags=["Telegram"])


@router.post(config.bot.WEBHOOK_ENDPOINT, include_in_schema=False)
async def webhook_handler(
    bot_id: int,
    update: types.Update,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(bot_manager.feed_update, bot_id, update)


@router.post(
    "/tg/add_bot",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new bot",
    response_description="Created Bot ID [from Telegram]",
    response_model=int,
)
async def add_bot(
    customer_id: UUID,
    data: AddBotModel,
    current_user: Annotated[User, Depends(security.get_current_user)],
):
    if not await user_service.user_can_add_bot(current_user.id, customer_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Available only to administrators",
        )
    bot_id = await bot_manager.add_bot(
        bot_token=data.token,
        owner_id=customer_id,
    )
    if bot_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid bot token",
        )
    return bot_id
