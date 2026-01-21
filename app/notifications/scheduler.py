import asyncio  # noqa: INP001
from datetime import datetime, timedelta, timezone
from typing import Any

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from config.bot import config

from .service import ReminderService


class ReminderScheduler:
    """Планировщик напоминаний"""

    def __init__(self, bot_token: str):
        self.bot = Bot(token=bot_token)
        self.service = ReminderService(self.bot)
        self.scheduler = AsyncIOScheduler(
            timezone="UTC",
            job_defaults={
                "coalesce": True,
                "max_instances": 3,
                "misfire_grace_time": 300,
            },
        )
        self.is_running = False

    async def start(self) -> None:
        """Запускает планировщик"""
        if self.is_running:
            return

        if not await self._check_telegram_connection():
            return

        trigger = IntervalTrigger(
            minutes=config.CHECK_INTERVAL,
            start_date=datetime.now(timezone.utc) + timedelta(seconds=10),
        )

        self.scheduler.add_job(
            self._check_and_send_reminders,
            trigger=trigger,
            id="check_reminders",
            name="Проверка и отправка напоминаний",
            replace_existing=True,
        )

        self.scheduler.start()
        self.is_running = True
        asyncio.create_task(self._check_and_send_reminders())  # noqa: RUF006

    async def stop(self) -> None:
        """Останавливает планировщик"""
        if not self.is_running:
            return
        self.scheduler.shutdown(wait=True)
        await self.bot.session.close()
        self.is_running = False

    async def _check_telegram_connection(self) -> bool:
        """Проверяет соединение c Telegram"""
        try:
            await self.bot.get_me()
            return True
        except Exception:  # noqa: BLE001
            return False

    async def _check_and_send_reminders(self):
        """Проверяет и отправляет напоминания"""
        await self.service.send_reminders()

    async def force_check(self) -> dict[str, Any]:
        """Принудительно запускает проверку напоминаний"""
        return await self.service.send_reminders()
