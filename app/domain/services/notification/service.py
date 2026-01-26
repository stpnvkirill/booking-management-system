import contextlib
from datetime import datetime
from typing import Any
import uuid
from zoneinfo import ZoneInfo

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot import bot_manager
from app.infrastructure.database.models.notification import (
    Notification,
    NotificationStatus,
)
from app.infrastructure.database.models.users import BotConfig, User
from app.log import log

from .factory import NotificationFactory


class NotificationService:
    """Service for sending notifications. Business logic of notification sending."""

    def __init__(self, session_factory):
        """Initialize notification service with database session factory."""
        self.session_factory = session_factory
        self._bot_cache = {}  # Cache: customer_id -> Bot

    async def send_booking_24h(self, notification: Notification) -> bool:
        """Send 24-hour booking reminder notification."""
        return await self._send_notification(notification)

    async def send_booking_1h(self, notification: Notification) -> bool:
        """Send 1-hour booking reminder notification."""
        return await self._send_notification(notification)

    async def send_booking_start(self, notification: Notification) -> bool:
        """Send booking start notification."""
        return await self._send_notification(notification)

    async def send_booking_end(self, notification: Notification) -> bool:
        """Send booking end notification."""
        return await self._send_notification(notification)

    async def _send_notification(  # noqa: PLR0912
        self,
        notification: Notification,
        session: AsyncSession = None,
    ) -> bool:
        external_session = session is not None
        if session is None:
            session = self.session_factory()

        try:
            notification.status = NotificationStatus.PROCESSING
            notification.processed_at = datetime.now(ZoneInfo("UTC"))
            await session.flush()

            # Get customer_id for notification
            customer_id = await self._get_customer_for_notification(notification)
            if not customer_id:
                await self._mark_as_failed(
                    notification,
                    session,
                    "Could not determine customer for notification",
                )
                if not external_session:
                    await session.commit()
                return False

            # Get bot for customer
            bot = await self._get_bot_for_customer(customer_id, session)
            if not bot:
                await self._mark_as_failed(
                    notification,
                    session,
                    f"Bot not found for customer {customer_id}",
                )
                if not external_session:
                    await session.commit()
                return False

            # Get booking data
            booking = notification.booking
            if not booking:
                await self._mark_as_failed(
                    notification,
                    session,
                    "Booking data not loaded",
                )
                if not external_session:
                    await session.commit()
                return False

            # Create message
            message = NotificationFactory.create_message(notification.type, booking)

            try:
                # Send message
                await self._send_telegram_message(
                    bot=bot,
                    user_id=notification.user_id,
                    message=message,
                )

                # Update status
                notification.status = NotificationStatus.SENT
                notification.message = message
                log(
                    level="info",
                    method="_send_notification",
                    path="NotificationService",
                    text_detail=f"Notification {notification.id} sent to user {notification.user_id}",  # noqa: E501
                )

                if not external_session:
                    await session.commit()

                return True

            except Exception as e:  # noqa: BLE001
                log(
                    level="error",
                    method="_send_notification",
                    path="NotificationService",
                    text_detail=f"Error sending notification {notification.id}: {e}",
                    exception=e,
                )
                await self._mark_as_failed(notification, session, str(e))
                if not external_session:
                    await session.commit()
                return False

        except Exception as e:  # noqa: BLE001
            log(
                level="error",
                method="_send_notification",
                path="NotificationService",
                text_detail=f"Unexpected error in send_notification: {e}",
                exception=e,
            )
            if not external_session:
                with contextlib.suppress(Exception):
                    await session.rollback()
            return False
        finally:
            if not external_session:
                await session.close()

    async def _get_customer_for_notification(
        self,
        notification: Notification,
    ) -> str | None:
        """Get customer ID for notification's booking resource."""
        try:
            if not notification.booking or not notification.booking.resource_obj:
                return None

            resource = notification.booking.resource_obj
            if not resource.customer_id:
                return None

            return str(resource.customer_id)

        except Exception as e:  # noqa: BLE001
            log(
                level="error",
                method="_get_customer_for_notification",
                path="NotificationService",
                text_detail=f"Error getting customer for notification: {e}",
                exception=e,
            )
            return None

    async def _get_bot_for_customer(  # noqa: PLR0911
        self,
        customer_id_str: str,
        session: AsyncSession,
    ) -> Any | None:
        """Get bot for customer from DB with caching."""
        # Check cache
        if customer_id_str in self._bot_cache:
            return self._bot_cache[customer_id_str]

        try:
            # Convert string to UUID
            try:
                customer_id_uuid = uuid.UUID(customer_id_str)
            except ValueError:
                log(
                    level="error",
                    method="_get_bot_for_customer",
                    path="NotificationService",
                    text_detail=f"Invalid UUID format for: {customer_id_str}",
                )
                return None

            # Find bot for this customer: get id and token
            stmt = (
                sa.select(BotConfig.id, BotConfig.token)
                .where(
                    BotConfig.owner_id == customer_id_uuid,
                )
                .limit(1)
            )

            row = await session.execute(stmt)
            res = row.first()
            if not res:
                log(
                    level="error",
                    method="_get_bot_for_customer",
                    path="NotificationService",
                    text_detail=f"BotConfig not found for customer {customer_id_str}",
                )
                return None

            bot_id, bot_token = res[0], res[1]

            # Try to get bot from BotManager
            bot = bot_manager.bots.get(bot_id)
            if bot:
                self._bot_cache[customer_id_str] = bot
                log(
                    level="debug",
                    method="_get_bot_for_customer",
                    path="NotificationService",
                    text_detail=f"Bot for customer {customer_id_str} obtained from BotManager",  # noqa: E501
                )
                return bot

            if not bot_token:
                log(
                    level="error",
                    method="_get_bot_for_customer",
                    path="NotificationService",
                    text_detail=f"Bot token not found for customer {customer_id_str}",
                )
                return None

            try:
                await bot_manager.start_bot(bot_id, bot_token)
                bot = bot_manager.bots.get(bot_id)
                if bot:
                    self._bot_cache[customer_id_str] = bot
                    log(
                        level="debug",
                        method="_get_bot_for_customer",
                        path="NotificationService",
                        text_detail=f"Customer Bot {customer_id_str} registered",
                    )
                    return bot
                log(
                    level="error",
                    method="_get_bot_for_customer",
                    path="NotificationService",
                    text_detail=f"Failed to get bot {customer_id_str}",
                )
                return None
            except Exception as e:  # noqa: BLE001
                log(
                    level="error",
                    method="_get_bot_for_customer",
                    path="NotificationService",
                    text_detail=f"Error starting bot BotManager{customer_id_str}: {e}",
                    exception=e,
                )
                return None

        except Exception as e:  # noqa: BLE001
            log(
                level="error",
                method="_get_bot_for_customer",
                path="NotificationService",
                text_detail=f"Error getting bot for customer {customer_id_str}: {e}",
                exception=e,
            )
            return None

    async def _send_telegram_message(self, bot: Any, user_id: str, message: str):
        """Send message via Telegram."""
        try:
            # user_id is UUID, need to find User by this UUID
            async with self.session_factory() as session:
                stmt = sa.select(User.tlg_id).where(User.id == user_id)
                tlg_id = await session.scalar(stmt)
                if not tlg_id:
                    msg = f"Telegram ID not found for user {user_id}"
                    raise ValueError(
                        msg,
                    )
                await bot.send_message(
                    chat_id=tlg_id,
                    text=message,
                    parse_mode="HTML",
                )
        except Exception as e:
            log(
                level="error",
                method="_send_telegram_message",
                path="NotificationService",
                text_detail=f"Error sending message: {e}",
                exception=e,
            )
            raise

    async def _mark_as_failed(
        self,
        notification: Notification,
        error: str,
    ):
        """Mark notification as failed."""
        notification.status = NotificationStatus.FAILED
        notification.error = error
        notification.processed_at = datetime.now(ZoneInfo("UTC"))

    async def clear_bot_cache(self):
        """Clear cached bot sessions."""
        for bot in self._bot_cache.values():
            try:
                await bot.session.close()
            except Exception as e:  # noqa: BLE001
                log(
                    level="error",
                    method="clear_bot_cache",
                    path="NotificationService",
                    text_detail=f"Error closing bot session: {e}",
                    exception=e,
                )
        self._bot_cache.clear()
