import asyncio  # noqa: INP001
from datetime import datetime, timedelta, timezone
from typing import Any

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError, TelegramForbiddenError
from config.bot import config
from depends import Provider
from infrastructure.database.models.booking import Booking as Mdl
import sqlalchemy as sa

from app.infrastructure.database.models.booking import Booking
from app.infrastructure.database.models.users import User

from .manager import NotificationManager, ReminderResult
from .messages import MessageFormatter


class ReminderService:
    """Сервис для отправки напоминаний"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.max_retries = 3
        self.retry_delay = 2
        self.message_formatter = MessageFormatter()

    @Provider.inject_session
    async def get_user_for_booking(self, booking: Booking, session=None):
        """Получает пользователя для бронирования"""
        try:
            stmt = sa.select(User).where(User.id == booking.user_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
        except (sa.exc.SQLAlchemyError, ValueError):
            return None

    @Provider.inject_session
    async def get_bookings_for_reminder(self, hours_before: int, session=None):
        try:
            now = datetime.now(timezone.utc)
            reminder_type = "24h" if hours_before == 24 else "1h"  # noqa: PLR2004

            window_start = (
                now
                + timedelta(hours=hours_before)
                - timedelta(minutes=config.CHECK_INTERVAL / 2)
            )
            window_end = (
                now
                + timedelta(hours=hours_before)
                + timedelta(minutes=config.CHECK_INTERVAL / 2)
            )

            stmt = sa.select(Booking).where(
                sa.and_(
                    Booking.start_time.between(window_start, window_end),
                    Booking.start_time > now,
                ),
            )

            result = await session.execute(stmt)
            bookings = result.scalars().all()

            filtered_bookings = []
            for booking in bookings:
                if not NotificationManager.is_notification_sent(
                    booking.id,
                    reminder_type,
                ):
                    filtered_bookings.append(booking)

            return filtered_bookings

        except (sa.exc.SQLAlchemyError, ValueError):
            return []

    @Provider.inject_session
    async def get_bookings_for_24h_reminder(self, session=None):
        return await self.get_bookings_for_reminder(24, session)

    @Provider.inject_session
    async def get_bookings_for_1h_reminder(self, session=None):
        return await self.get_bookings_for_reminder(1, session)

    async def send_telegram_message(
        self,
        chat_id: int,
        message: str,
        parse_mode: str = "HTML",
    ) -> bool:
        """Отправляет сообщение в Telegram."""
        for attempt in range(self.max_retries):
            try:
                await self.bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode=parse_mode,
                    disable_web_page_preview=True,
                )
                return True

            except TelegramForbiddenError:
                return False
            except TelegramAPIError:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                continue
            except (ValueError, TypeError):
                return False

        return False

    async def send_24h_reminders(self) -> list[ReminderResult]:
        """Отправляет напоминания за 24 часа"""
        if not Mdl.is_24h_notification_due():
            return []

        bookings = await self.get_bookings_for_24h_reminder()
        results = []

        for booking in bookings:
            try:
                if Mdl.is_current(booking):
                    continue
                if not Mdl.is_upcoming(booking):
                    continue

                user = await self.get_user_for_booking(booking)
                if not user or not user.tlg_id:
                    continue

                if not Mdl.is_active(booking):
                    continue
                if Mdl.is_completed(booking):
                    continue

                message = self.message_formatter.format_24h_message(booking, user)
                success = await self.send_telegram_message(
                    chat_id=user.tlg_id,
                    message=message,
                    parse_mode="HTML",
                )

                if success:
                    NotificationManager.mark_notification_sent(booking.id, "24h")

                results.append(
                    ReminderResult(
                        booking_id=booking.id,
                        user_id=user.id,
                        success=success,
                        error_message=None
                        if success
                        else "Ne udalos' otpravit' soobshenie",
                    ),
                )

            except (ValueError, TypeError, sa.exc.SQLAlchemyError) as e:
                results.append(
                    ReminderResult(
                        booking_id=booking.id,
                        user_id=booking.user_id,
                        success=False,
                        error_message=str(e),
                    ),
                )

        return results

    async def send_1h_reminders(self) -> list[ReminderResult]:
        """Отправляет напоминания за 1 час"""
        if not Mdl.is_1h_notification_due():
            return []

        bookings = await self.get_bookings_for_1h_reminder()
        results = []

        for booking in bookings:
            try:
                if Mdl.is_current(booking):
                    continue
                if not Mdl.is_upcoming(booking):
                    continue
                if Mdl.is_completed(booking):
                    continue
                if not Mdl.is_active(booking):
                    continue

                user = await self.get_user_for_booking(booking)
                if not user or not user.tlg_id:
                    continue

                message = self.message_formatter.format_1h_message(booking, user)
                success = await self.send_telegram_message(
                    chat_id=user.tlg_id,
                    message=message,
                    parse_mode="HTML",
                )

                if success:
                    NotificationManager.mark_notification_sent(booking.id, "1h")

                results.append(
                    ReminderResult(
                        booking_id=booking.id,
                        user_id=user.id,
                        success=success,
                        error_message=None
                        if success
                        else "Ne udalos' otpravit' soobshenie",
                    ),
                )

            except (ValueError, TypeError, sa.exc.SQLAlchemyError) as e:
                results.append(
                    ReminderResult(
                        booking_id=booking.id,
                        user_id=booking.user_id,
                        success=False,
                        error_message=str(e),
                    ),
                )

        return results

    async def send_reminders(self) -> dict[str, Any]:
        """Отправляет все напоминания"""
        start_time = datetime.now(timezone.utc)

        results_24h = await self.send_24h_reminders()
        results_1h = await self.send_1h_reminders()

        total_sent = sum(1 for r in results_24h + results_1h if r.success)
        total_processed = len(results_24h) + len(results_1h)
        execution_time = (datetime.now(timezone.utc) - start_time).total_seconds()

        return {
            "24h": results_24h,
            "1h": results_1h,
            "total_sent": total_sent,
            "total_processed": total_processed,
            "execution_time": execution_time,
            "timestamp": start_time.isoformat(),
        }
