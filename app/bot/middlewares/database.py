from collections.abc import Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, InlineQuery, Message, Update
from sqlalchemy.ext.asyncio import AsyncSession

from app.depends import provider


class DatabaseMiddleware(BaseMiddleware):
    """Middleware для предоставления сессии БД в контексте обработчиков."""

    async def __call__(
        self,
        handler: Callable,
        event: Message | CallbackQuery | InlineQuery | Update,
        data: dict,
    ):
        async with provider.session_factory() as session:
            data["session"] = session
            try:
                result = await handler(event, data)
                await session.commit()
                return result
            except Exception:
                await session.rollback()
                raise
            
