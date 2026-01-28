from collections.abc import Callable
import time

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, InlineQuery, Message, Update

from app.metrics.business import (
    bot_message_processing_seconds,
    bot_messages_total,
)


class MetricsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable,
        event: Update | Message | CallbackQuery | InlineQuery,
        data: dict,
    ):
        start_time = time.time()
        bot_id = str(event.bot.id)
        handler_name = self._get_handler_name(handler, data)

        if handler_name is None:
            handler_name = "unknown"

        chat_type = self._get_chat_type(event)

        try:
            return await handler(event, data)
        finally:
            processing_time = time.time() - start_time

            bot_messages_total.labels(
                bot_id=bot_id,
                chat_type=chat_type,
                handler=handler_name,
            ).inc()

            bot_message_processing_seconds.labels(
                bot_id=bot_id,
                handler=handler_name,
            ).observe(processing_time)

    @staticmethod
    def _get_handler_name(handler: Callable, data: dict) -> str | None:
        event_handler = data.get("event_handler")

        if event_handler and hasattr(event_handler, "callback"):
            return event_handler.callback.__name__

        return getattr(handler, "__name__", None) or handler.__class__.__name__

    @staticmethod
    def _get_chat_type(event) -> str:
        chat_type = "unknown"

        if isinstance(event, Message):
            chat_type = event.chat.type

        elif isinstance(event, CallbackQuery):
            if event.message and event.message.chat:
                chat_type = event.message.chat.type
            else:
                chat_type = "callback_without_message"

        elif isinstance(event, InlineQuery):
            chat_type = "inline"

        elif isinstance(event, Update):
            for field in (
                "message",
                "edited_message",
                "channel_post",
                "edited_channel_post",
            ):
                msg = getattr(event, field, None)
                if msg and msg.chat:
                    return msg.chat.type

            return event.event_type

        return chat_type
