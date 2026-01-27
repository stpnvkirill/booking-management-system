from collections.abc import Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from app.depends import provider


class SessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable,
        event: Message | CallbackQuery,
        data: dict,
    ):
        async with provider.session_factory() as session:
            data["session"] = session
            try:
                result = await handler(event, data)
                if result is not None:
                    await session.commit()
                return result
            except Exception:
                await session.rollback()
                raise
