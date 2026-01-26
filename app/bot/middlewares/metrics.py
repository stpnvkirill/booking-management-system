"""Middleware for collecting bot metrics."""

from collections.abc import Callable
import time

from aiogram import BaseMiddleware, types

from app.metrics.business import (
    bot_message_processing_seconds,
    bot_messages_total,
)


class MetricsMiddleware(BaseMiddleware):
    """Middleware to collect bot metrics for Prometheus."""

    async def __call__(
        self,
        handler: Callable,
        event: types.Message | types.CallbackQuery | types.InlineQuery | types.Update,
        data: dict,
    ):
        """Collect metrics for bot messages."""
        start_time = time.time()
        bot_id = str(event.bot.id)

        # Determine event type and handler name
        handler_name = getattr(handler, "__name__", "unknown")
        chat_type = "unknown"

        try:
            if event.message:
                chat_type = event.message.chat.type if event.message.chat else "unknown"
            elif event.callback_query:
                if event.callback_query.message:
                    chat_type = (
                        event.callback_query.message.chat.type
                        if event.callback_query.message.chat
                        else "unknown"
                    )
            elif event.inline_query:
                chat_type = "inline"
        except Exception:  # noqa: BLE001, S110
            pass

        try:
            result = await handler(event, data)
            processing_time = time.time() - start_time

            # Record metrics
            bot_messages_total.labels(
                bot_id=bot_id,
                chat_type=chat_type,
                handler=handler_name,
            ).inc()

            bot_message_processing_seconds.labels(
                bot_id=bot_id,
                handler=handler_name,
            ).observe(processing_time)

            return result
        except Exception:
            # Still record metrics even on error
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

            raise
