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
from sqlalchemy.orm import selectinload

from app.infrastructure.database.models.booking import Booking, Resource
from app.infrastructure.database.models.notification import (
    Notification,
    NotificationStatus,
)
from app.infrastructure.database.models.users import BotConfig, Customer, User
from app.notification.factory import NotificationFactory

logger = logging.getLogger(__name__)


class NotificationScheduler:
    """Планировщик для отправки уведомлений."""

    def __init__(self, session_factory):
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
        self._bot_cache = {}  # Кэш: customer_id -> Bot

    async def start(self) -> None:
        """Запускает планировщик."""
        if self.is_running:
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
        logger.info("Планировщик уведомлений запущен")
        # Первый запуск через 5 секунд
        asyncio.create_task(self._process_notifications_job())

    async def stop(self) -> None:
        """Останавливает планировщик."""
        if not self.is_running:
            return
        self.scheduler.shutdown(wait=True)
        
        # Закрываем все кэшированные сессии ботов
        for bot in self._bot_cache.values():
            try:
                await bot.session.close()
            except Exception as e:
                logger.error(f"Ошибка закрытия сессии бота: {e}")
        
        self._bot_cache.clear()
        self.is_running = False
        logger.info("Планировщик уведомлений остановлен")

    async def _process_notifications_job(self):
        """Основная задача обработки уведомлений."""
        try:
            async with self.session_factory() as session:
                notifications = await self._get_pending_notifications(session)

                if not notifications:
                    logger.debug("Нет уведомлений для отправки")
                    return

                logger.info(f"Найдено {len(notifications)} уведомлений для обработки")

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
            .options(
                selectinload(Notification.booking).selectinload(Booking.resource_obj),
                selectinload(Notification.user)
            )
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
        session: AsyncSession,
    ):
        """Обрабатывает одно уведомление."""
        notification.status = NotificationStatus.PROCESSING
        notification.processed_at = datetime.now(ZoneInfo("UTC"))
        await session.flush()

        customer_id = await self._get_customer_for_notification(notification)
        if not customer_id:
            await self._mark_as_failed(
                notification, session,
                "Не удалось определить customer для уведомления"
            )
            return

        # Получаем токен бота для этого кастомера из БД
        bot = await self._get_bot_for_customer(customer_id, session)
        if not bot:
            await self._mark_as_failed(
                notification, session,
                f"Бот не найден для customer {customer_id}"
            )
            return

        # Получаем данные бронирования
        booking = notification.booking
        if not booking:
            await self._mark_as_failed(
                notification, session,
                "Данные бронирования не загружены"
            )
            return

        # Формируем сообщение
        message = NotificationFactory.create_message(notification.type, booking)

        try:
            # Отправляем сообщение
            await self._send_telegram_message(
                bot=bot,
                user_id=notification.user_id,
                message=message
            )
            
            # Обновляем статус
            notification.status = NotificationStatus.SENT
            notification.message = message
            logger.info(f"Уведомление {notification.id} отправлено пользователю {notification.user_id} через бота кастомера {customer_id}")
            
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления {notification.id}: {e}")
            await self._mark_as_failed(notification, session, str(e))

    async def _get_customer_for_notification(self, notification: Notification) -> str | None:
        """Получает customer_id для уведомления через цепочку таблиц."""
        try:
            # notification → booking → resource → customer
            if not notification.booking or not notification.booking.resource_obj:
                return None
                
            resource = notification.booking.resource_obj
            if not resource.customer_id:
                return None
                
            return str(resource.customer_id)
            
        except Exception as e:
            logger.error(f"Ошибка получения customer для уведомления: {e}")
            return None

    async def _get_bot_for_customer(self, customer_id: str, session: AsyncSession) -> Bot | None:
        """Получает бота для кастомера из БД с кэшированием."""
        # Проверяем кэш
        if customer_id in self._bot_cache:
            return self._bot_cache[customer_id]

        try:
            stmt = sa.select(BotConfig.token).where(
                BotConfig.owner_id == customer_id,
                BotConfig.token.is_not(None)
            ).limit(1)
            
            bot_token = await session.scalar(stmt)
            
            if not bot_token:
                logger.error(f"Токен бота не найден для customer {customer_id}")
                return None
            
            # Создаем бота
            bot = Bot(token=bot_token)
            
            # Проверяем соединение
            try:
                await bot.get_me()
            except Exception as e:
                logger.error(f"Бот недоступен для customer {customer_id}: {e}")
                return None
            
            # Сохраняем в кэш
            self._bot_cache[customer_id] = bot
            logger.debug(f"Бот для customer {customer_id} закэширован")
            
            return bot
            
        except Exception as e:
            logger.error(f"Ошибка получения бота для customer {customer_id}: {e}")
            return None

    async def _send_telegram_message(self, bot: Bot, user_id: int, message: str):
        """Отправляет сообщение через Telegram."""
        # Получаем tlg_id пользователя
        try:
            async with self.session_factory() as session:
                stmt = sa.select(User.tlg_id).where(User.id == user_id)
                tlg_id = await session.scalar(stmt)
                
                if not tlg_id:
                    raise ValueError(f"Telegram ID не найден для пользователя {user_id}")
                
                await bot.send_message(
                    chat_id=tlg_id,
                    text=message,
                    parse_mode="HTML"
                )
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения: {e}")
            raise

    async def _mark_as_failed(
        self, 
        notification: Notification,
        session: AsyncSession,
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
