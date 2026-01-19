import asyncio  # noqa: INP001
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError, TelegramForbiddenError
from depends import Provider
import sqlalchemy as sa

from app.infrastructure.database.models.booking import Booking
from app.infrastructure.database.models.users import User

from .config import Config
from .models import Booking_cl as mdl

config = Config()


def get_db():
    """Получает сессию базы данных через Provider"""

    @Provider.inject_session
    async def get_session(session=None):
        return session

    return get_session()


@dataclass
class ReminderResult:
    """Результат отправки напоминания"""

    booking_id: int
    user_id: int
    success: bool
    error_message: str | None = None


class NotificationManager:
    """Менеджер для управления состоянием уведомлений"""

    # Временное хранилище для отправленных уведомлений (в продакшене заменить на БД)
    _sent_notifications = set()  # noqa: RUF012

    @classmethod
    def is_notification_sent(cls, booking_id: int, reminder_type: str) -> bool:
        """Проверяет, было ли отправлено уведомление"""
        key = f"{booking_id}_{reminder_type}"
        return key in cls._sent_notifications

    @classmethod
    def mark_notification_sent(cls, booking_id: int, reminder_type: str):
        """Отмечает уведомление как отправленное"""
        key = f"{booking_id}_{reminder_type}"
        cls._sent_notifications.add(key)


class ReminderService:
    """Сервис для отправки напоминаний"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.max_retries = 3
        self.retry_delay = 2

    def _format_duration(self, booking: Booking) -> str:
        """Форматирует длительность бронирования"""
        if hasattr(booking, "end_time") and booking.end_time:
            duration = booking.end_time - booking.start_time
            hours = duration.total_seconds() // 3600
            minutes = (duration.total_seconds() % 3600) // 60

            if hours > 0:
                return f"{int(hours)} ch {int(minutes)} min"
            return f"{int(minutes)} min"
        return "1 chas"

    def _format_24h_message(self, booking: Booking, user: User) -> str:
        """Форматирует сообщение для 24-часового напоминания"""
        start_time = booking.start_time.strftime("%d.%m.%Y v %H:%M")
        user_name = user.first_name or user.username or "Uvazhaemyj klient"
        duration_text = self._format_duration(booking)

        return (
            f"🔔 <b>Napominanie o bronirovanii</b>\n\n"
            f"Zdravstvujte, {user_name}!\n\n"
            f"Cherez 24 chasa u vas zapolneno bronirovanie:\n"
            f"🕐 <b>Vremya nachala:</b> {start_time}\n"
            f"⏳ <b>Prodolzhitel'nost':</b> {duration_text}\n\n"
            f"Pozhalujsta, podtverdite vashe uchastie.\n"
        )

    def _format_1h_message(self, booking: Booking, user: User) -> str:
        """Форматирует сообщение для 1-часового напоминания"""
        start_time = booking.start_time.strftime("%H:%M")
        user_name = user.first_name or user.username or "Uvazhaemyj klient"
        duration_text = self._format_duration(booking)

        return (
            f"⏰ <b>Skoro nachinaem!</b>\n\n"
            f"{user_name}, napominaem, chto cherez 1 chas:\n"
            f"🕐 <b>Nachalo v:</b> {start_time}\n"
            f"⏳ <b>Prodolzhitel'nost':</b> {duration_text}\n\n"
            f"Rekomenduem pribyt' za 10-15 minut do nachala."
        )

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
        """Получает бронирования для напоминания за указанное количество часов"""
        try:
            now = datetime.now(timezone.utc)
            reminder_type = "24h" if hours_before == 24 else "1h"  # noqa: PLR2004

            # Вычисляем временное окно: часы до брони ± половина интервала проверки
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

            # Получаем бронирования в этом временном окне
            stmt = sa.select(Booking).where(
                sa.and_(
                    Booking.start_time.between(window_start, window_end),
                    Booking.start_time > now,  # Только будущие брони
                ),
            )

            result = await session.execute(stmt)
            bookings = result.scalars().all()

            # Фильтруем те, которым уже отправляли напоминания
            filtered_bookings = []
            for booking in bookings:
                if not mdl.is_active(booking):
                    continue
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
        """Получает бронирования для 24-часового напоминания"""
        return await self.get_bookings_for_reminder(24, session)

    @Provider.inject_session
    async def get_bookings_for_1h_reminder(self, session=None):
        """Получает бронирования для 1-часового напоминания"""
        return await self.get_bookings_for_reminder(1, session)

    async def send_telegram_message(
        self,
        chat_id: int,
        message: str,
        parse_mode: str = "HTML",
    ) -> bool:
        """
        Отправляет сообщение в Telegram.
        """
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
        bookings = await self.get_bookings_for_24h_reminder()
        results = []

        if not mdl.is_24h_notification_due():
            return results
        if not bookings:
            return results

        for booking in bookings:
            try:
                user = await self.get_user_for_booking(booking)

                if not mdl.is_active(booking):
                    continue
                if not user or not user.tlg_id:
                    continue

                message = self._format_24h_message(booking, user)
                success = await self.send_telegram_message(
                    chat_id=user.tlg_id,
                    message=message,
                    parse_mode="HTML",
                )

                if success:
                    NotificationManager.mark_notification_sent(booking.id, "24h")

                result = ReminderResult(
                    booking_id=booking.id,
                    user_id=user.id,
                    success=success,
                    error_message=None
                    if success
                    else "Ne udalos' otpravit' soobshenie",
                )
                results.append(result)

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
        bookings = await self.get_bookings_for_1h_reminder()
        results = []

        if not mdl.is_1h_notification_due():
            return results
        if not bookings:
            return results

        for booking in bookings:
            try:
                if not mdl.is_active(booking):
                    continue
                user = await self.get_user_for_booking(booking)
                if not user or not user.tlg_id:
                    continue

                message = self._format_1h_message(booking, user)
                success = await self.send_telegram_message(
                    chat_id=user.tlg_id,
                    message=message,
                    parse_mode="HTML",
                )

                if success:
                    NotificationManager.mark_notification_sent(booking.id, "1h")

                result = ReminderResult(
                    booking_id=booking.id,
                    user_id=user.id,
                    success=success,
                    error_message=None
                    if success
                    else "Ne udalos' otpravit' soobshenie",
                )
                results.append(result)

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

    async def send_reminders(self, log_notification: bool = True) -> dict[str, Any]:  # noqa: ARG002
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


class ReminderScheduler:
    """Планировщик напоминаний"""

    def __init__(self, bot_token: str):
        self.bot = Bot(token=bot_token)
        self.service = ReminderService(self.bot)
        self.is_running = False
