import asyncio
from datetime import datetime, timedelta
import logging
from typing import Any
from zoneinfo import ZoneInfo

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import sqlalchemy as sa
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.notification import (
    Notification,
    NotificationStatus,
)
from app.notification.factory import NotificationFactory

logger = logging.getLogger(__name__)


class NotificationScheduler:
    """Планировщик для отправки уведомлений."""

    def __init__(self, bot_token: str, session_factory):
        self.bot = Bot(token=bot_token)
        self.session_factory = session_factory
        self.scheduler = AsyncIOScheduler(
            timezone="UTC",
            job_defaults={
                "coalesce": True,
                "max_instances": 3,
                "misfire_grace_time": 300,
            },
        )
        self.is_running = False
        self.check_interval = 5  # минут
        self.batch_size = 50

    async def start(self) -> None:
        """Запускает планировщик."""
        if self.is_running:
            return

        if not await self._check_telegram_connection():
            logger.error("Не удалось подключиться к Telegram")
            return

        trigger = IntervalTrigger(
            minutes=self.check_interval,
            start_date=datetime.now(ZoneInfo("UTC")) + timedelta(seconds=10),
        )

        self.scheduler.add_job(
            self._process_notifications_job,
            trigger=trigger,
            id="process_notifications",
            name="Отправка уведомлений",
            replace_existing=True,
        )

        self.scheduler.start()
        self.is_running = True
        # Первый запуск через 5 секунд
        asyncio.create_task(self._process_notifications_job())

    async def stop(self) -> None:
        """Останавливает планировщик."""
        if not self.is_running:
            return
        self.scheduler.shutdown(wait=True)
        await self.bot.session.close()
        self.is_running = False
        logger.info("Планировщик уведомлений остановлен")

    async def _check_telegram_connection(self) -> bool:
        """Проверяет соединение с Telegram."""
        try:
            await self.bot.get_me()
            return True
        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка подключения к Telegram: {e}")
            return False

    async def _process_notifications_job(self):
        """Основная задача обработки уведомлений."""
        try:
            async with self.session_factory() as session:
                notifications = await self._get_pending_notifications(session)

                if not notifications:
                    logger.debug("Нет уведомлений для отправки")
                    return

                for notification in notifications:
                    try:
                        await self._process_single_notification(notification, session)
                    except Exception as e:  # noqa: BLE001
                        logger.error(f"Ошибка обработки уведомления {notification.id}: {e}")
                        await self._mark_as_failed(notification, session, str(e))

                await session.commit()

        except Exception as e:  # noqa: BLE001
            logger.error(f"Ошибка в задаче обработки уведомлений: {e}")

    async def _get_pending_notifications(self, session: AsyncSession) -> list[Notification]:
        """Получает уведомления, готовые к отправке."""
        now = datetime.now(ZoneInfo("UTC"))
        stmt = (
            sa.select(Notification)
            .where(
                and_(
                    Notification.status == NotificationStatus.PENDING,
                    Notification.scheduled_at <= now,
                    Notification.scheduled_at >= now - timedelta(hours=24),
                ),
            )
            .order_by(Notification.scheduled_at)
            .limit(self.batch_size)
        )

        result = await session.scalars(stmt)
        return result.all()

    async def _process_single_notification(
        self, 
        notification: Notification, 
        session: AsyncSession
    ):
        """Обрабатывает одно уведомление."""
        # Обновляем статус на "в обработке"
        notification.status = NotificationStatus.PROCESSING
        notification.processed_at = datetime.now(ZoneInfo("UTC"))
        await session.flush()

        # Получаем данные бронирования
        booking = notification.booking

        # Формируем сообщение
        message = NotificationFactory.create_message(notification.type, booking)

        try:
            # Отправляем сообщение
            await self._send_telegram_message(
                user_id=notification.user_id,
                message=message
            )
            
            # Обновляем статус
            notification.status = NotificationStatus.SENT
            notification.message = message
            logger.info(f"Уведомление {notification.id} отправлено пользователю {notification.user_id}")
            
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления {notification.id}: {e}")
            await self._mark_as_failed(notification, session, str(e))

    async def _send_telegram_message(self, user_id: int, message: str):
        """Отправляет сообщение через Telegram."""
        await self.bot.send_message(
            chat_id=user_id,
            text=message,
            parse_mode="HTML"
        )

    async def _mark_as_failed(
        self, 
        notification: Notification, 
        error: str
    ):
        """Помечает уведомление как неудачное."""
        notification.status = NotificationStatus.FAILED
        notification.error = error
        notification.processed_at = datetime.now(ZoneInfo("UTC"))

    async def force_check(self) -> dict[str, Any]:
        """Принудительно запускает обработку уведомлений."""
        try:
            await self._process_notifications_job()
            return {"status": "success", "message": "Проверка уведомлений выполнена"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
