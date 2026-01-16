import asyncio  # noqa: INP001
from dataclasses import dataclass
from typing import Any

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError, TelegramForbiddenError
from depends import Provider as provider  # noqa: N813
from fastapi import logger
import sqlalchemy as sa

from app.infrastructure.database.models.users import User

from .config import Config

config = Config()


def get_db():
    """Получает сессию базы данных"""


class Booking:
    """Модель бронирования (заглушка)"""

    id: int
    user_id: int
    start_time: Any  # Замените на соответствующий тип времени


@dataclass
class ReminderResult:
    """Результат отправки напоминания"""

    booking_id: int
    user_id: int
    success: bool
    error_message: str | None = None


class ReminderService:
    """Сервис для отправки напоминаний"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @provider.inject_session
    async def get_user_for_booking(self, booking: Booking, session=None):
        """Получает пользователя для бронирования"""
        try:
            stmt = sa.select(User).where(User.id == booking.user_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:  # noqa: BLE001
            logger.error(
                f"Ошибка при получении пользователя для брони {booking.id}: {e}",
            )
            return None

    @provider.inject_session
    async def get_bookings_for_24h_reminder(self, session=None):
        """Получает бронирования для 24-часового напоминания"""
        return await self.get_bookings_for_reminder(24, session)

    @provider.inject_session
    async def get_bookings_for_1h_reminder(self, session=None):
        """Получает бронирования для 1-часового напоминания"""
        return await self.get_bookings_for_reminder(1, session)

    async def send_24h_reminders(self, chat_id: int, message: str) -> None:
        """Отправляет напоминания за 24 часа"""
        await self.send_telegram_message(chat_id=chat_id, message=message)

    async def send_1h_reminders(self, chat_id: int, message: str) -> None:  # noqa: ARG002
        """Отправляет напоминания за 1 час"""
        bookings = await self.get_bookings_for_24h_reminder()
        results = []

        if not bookings:
            logger.info("Нет бронирований для 24h напоминания")
            return results
        return None

    async def send_reminders(self, log_notification: bool = True) -> dict[str, Any]:  # noqa: ARG002
        """Отправляет все напоминания"""
        # Реализовать логику
        return None

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
                logger.debug(f"Сообщение отправлено пользователю {chat_id}")
                return True

            except TelegramForbiddenError:
                logger.warning(f"Пользователь {chat_id} заблокировал бота")
                return False
            except TelegramAPIError as e:
                logger.warning(
                    f"Попытка {attempt + 1}/{self.max_retries} не удалась: {e}",
                )
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                continue
            except Exception as e:  # noqa: BLE001
                logger.error(f"Неожиданная ошибка отправки: {e}")
                return False

        return False


class ReminderScheduler:
    """Планировщик напоминаний"""

    def __init__(self, bot_token: str):
        self.bot = Bot(token=bot_token)
        self.service = ReminderService(self.bot)
        self.is_running = False

    async def start(self) -> None:
        self.is_running = False

    async def stop(self) -> None:
        if not self.is_running:
            return

    async def _check_and_send_reminders(self):
        """Проверяет и отправляет напоминания"""
        logger.info("⏰ Запуск плановой проверки напоминаний...")

        try:
            results = await self.service.send_reminders()

            success_24h = sum(1 for r in results["24h"] if r.success)
            success_1h = sum(1 for r in results["1h"] if r.success)

            if results["total_processed"] > 0:
                logger.info(
                    f"✅ Проверка завершена за {results['execution_time']:.2f}с: "  # noqa: RUF001
                    f"24h: {success_24h}/{len(results['24h'])} успешно, "
                    f"1h: {success_1h}/{len(results['1h'])} успешно",
                )
            else:
                logger.info("✅ Проверка завершена: новых напоминаний нет")

        except Exception as e:  # noqa: BLE001
            logger.error(f"❌ Ошибка при проверке напоминаний: {e}")
