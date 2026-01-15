from dataclasses import dataclass  # noqa: INP001
from typing import Any

from aiogram import Bot


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

    async def send_24h_reminders(self, chat_id: int, message: str) -> None:
        """Отправляет напоминания за 24 часа"""
        await self.send_telegram_message(chat_id=chat_id, message=message)

    async def send_1h_reminders(self, chat_id: int, message: str) -> None:
        """Отправляет напоминания за 1 час"""
        await self.send_telegram_message(chat_id=chat_id, message=message)

    async def send_reminders(self, log_notification: bool = True) -> dict[str, Any]:  # noqa: ARG002
        """Отправляет все напоминания"""
        # Реализовать логику
        return {"24h": [], "1h": []}

    async def send_telegram_message(
        self,
        chat_id: int,  # noqa: ARG002
        message: str,  # noqa: ARG002
        parse_mode: str = "HTML",  # noqa: ARG002
    ) -> bool:
        """
        Отправляет сообщение в Telegram.

        Args:
            chat_id: ID чата пользователя
            message: Текст сообщения
            parse_mode: Режим парсинга (HTML, Markdown)
        """
        # Реализовать отправку
        return False


class ReminderScheduler:
    """Планировщик напоминаний"""

    def __init__(self, bot_token: str):
        self.bot = Bot(token=bot_token)
        self.service = ReminderService(self.bot)
        self.is_running = False

    async def start(self) -> None:
        self.is_running = True

    async def stop(self) -> None:
        if not self.is_running:
            return

    async def _check_and_send_reminders(self):
        pass
