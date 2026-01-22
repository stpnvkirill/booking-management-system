from collections.abc import Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, InlineQuery, Message, Update

from app.domain.services import user_service


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable,
        event: Message | CallbackQuery | InlineQuery | Update,
        data: dict,
    ):
        from_user = None
        if event.message:
            mess = event.message
            from_user = mess.from_user
        elif event.callback_query:
            cc = event.callback_query
            from_user = cc.from_user

        if from_user:
            user = await user_service.update_user_from_tlg(
                tlg_user=from_user,
                bot_id=event.bot.id,
            )
            data["user"] = user
        await handler(event, data)
