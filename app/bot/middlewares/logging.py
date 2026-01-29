from collections.abc import Callable
import math
import time

from aiogram import BaseMiddleware, types

from app.log import log

exclude_tg_user = [
    "added_to_attachment_menu",
    "can_join_groups",
    "can_read_all_group_messages",
    "supports_inline_queries",
    "can_connect_to_business",
    "has_main_web_app",
    "has_topics_enabled",
]


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable,
        event: types.Message | types.CallbackQuery | types.InlineQuery | types.Update,
        data: dict,
    ):
        start_time = time.time()
        try:
            if event.message:
                _type = "message"
                user = event.message.from_user
            elif event.callback_query:
                _type = "callback_query"
                user = event.callback_query.from_user
            elif event.inline_query:
                _type = "inline_query"
                user = event.inline_query.from_user
            else:
                _type = "update"
                user = None
        except:  # noqa: E722
            _type = "?"
            user = None
        try:
            res = await handler(event, data)
            log(
                level="INFO",
                method=f"TG:{_type}",
                path="logging_middleware",
                duration=math.ceil((time.time() - start_time) * 1000),
                user=user.model_dump(exclude=exclude_tg_user, exclude_none=True)
                if user
                else None,
                bot_id=event.bot.id,
                bot_username=event.bot._me.username,  # noqa: SLF001
            )
            return res
        except Exception as err:  # noqa: BLE001
            log(
                level="ERROR",
                method=f"TG:{_type}",
                path="logging_middleware",
                duration=math.ceil((time.time() - start_time) * 1000),
                user=user.model_dump(
                    exclude=exclude_tg_user,
                    exclude_none=True,
                )
                if user
                else None,
                exception=err,
                bot_id=event.bot.id,
                bot_username=event.bot._me.username,  # noqa: SLF001
            )
