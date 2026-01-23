Oooooooooo
ihotx1tle
В голосовом чате

Попов Никита — Вчера, в 11:28
from datetime import datetime
from typing import TYPE_CHECKING
import uuid as uuid_lib
from zoneinfo import ZoneInfo

import sqlalchemy as sa
Раскрыть
notification.py
4 кб
Козлов Никита

 — Вчера, в 11:29
всё ворк ?
Попов Никита — Вчера, в 11:29
это бд
там по мелочи исправил
Козлов Никита

 — Вчера, в 11:29
окей
по файлам всё ок?
Попов Никита — Вчера, в 11:29
щас скину файл где вызывать
щас еще скину погоди
Попов Никита — Вчера, в 11:45
@Козлов Никита
бля короче
на
def get_application() -> FastAPI:
    from .config import config  # noqa: PLC0415

    swagger_url = None
    openapi_url = None
    redoc_url = None


    scheduler = NotificationScheduler(config.bot.TEST_BOT_TOKEN)

    if config.server.SWAGGER_ENABLE:
        swagger_url = "/docs"
        openapi_url = "/openapi.json"


    async def startup_tasks():
        await scheduler.start()

    async def shutdown_tasks():
        await scheduler.stop()

    application = FastAPI(
        title=config.server.SERVER_NAME,
        description=config.server.SERVER_DESCRIPTION,
        debug=config.server.DEBUG,
        version=config.server.API_VERSION,
        docs_url=swagger_url,
        openapi_url=openapi_url,
        redoc_url=redoc_url,
        responses=config.server.server_responces,
        swagger_ui_parameters=config.server.swagger_ui_parameters,
        on_startup=[bot_manager.run_all, user_service.create_test_user,scheduler.start],
        on_shutdown=[bot_manager.stop_all,scheduler.stop],
    )

    application.middleware("http")(LoggingMiddleware())
    for route in routes:
        application.include_router(route, prefix="/api")

    Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=False,
    ).instrument(application).expose(application, include_in_schema=False)

    return application
в app.py засунб и должно воркать
либо проверь сам уже я заебался
и всё вроде всё
Козлов Никита

 — Вчера, в 11:48
Всё заливаю?
Остальное ок всё?
Попов Никита — Вчера, в 11:50
Вроде да
Козлов Никита

 — Вчера, в 11:51
https://github.com/stpnvkirill/booking-management-system/pull/23
GitHub
Notification by x1tle · Pull Request #23 · stpnvkirill/booking-ma...
Notification by x1tle · Pull Request #23 · stpnvkirill/booking-ma...
0
Попов Никита — Вчера, в 11:54
что
описание бы сделал какое нибкдь хотяб
Козлов Никита

 — Вчера, в 12:02
какое?
@Матвей Саширин сделай быстро описание я добавлю
Матвей Саширин — Вчера, в 12:08
какое?
Попов Никита — Вчера, в 12:24
ну что сделали
кто сделал
Козлов Никита

 — Вчера, в 13:06
https://github.com/stpnvkirill/booking-management-system/pull/23
GitHub
Notification by x1tle · Pull Request #23 · stpnvkirill/booking-ma...
📌 Цель изменений
Создание надежной системы асинхронных уведомлений для отправки напоминаний о бронированиях через Telegram, обеспечивающей автоматическую фоновую обработку и отслеживание ...
📌 Цель изменений
Создание надежной системы асинхронных уведомлений для отправки напоминаний о бронированиях через Telegram, обеспечивающей автоматическую фоновую обработку и отслеживание статусов.
...
нам пиздаааа
Начинаем исправлять
вы с базой данных начинайте
и дальше идите
мы попозже подключимся
кидайте все файлы сюда
Козлов Никита

 — Вчера, в 13:16
Начинайте с бд короче
import asyncio
from datetime import datetime, timedelta
import logging
from typing import Any
from zoneinfo import ZoneInfo
Раскрыть
message.txt
8 кб
import logging

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.notification.scheduler import NotificationScheduler

from .api import routes
from .bot import bot_manager
from .domain.services import user_service
from .middlewares import LoggingMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)

for logger_name in ["aiogram", "aiogram.event", "aiogram.dispatcher", "httpx"]:
    logging.getLogger(logger_name).setLevel(logging.WARNING)


def get_application() -> FastAPI:
    from .config import config  # noqa: PLC0415

    swagger_url = None
    openapi_url = None
    redoc_url = None


    scheduler = NotificationScheduler(config.bot.TEST_BOT_TOKEN)

    if config.server.SWAGGER_ENABLE:
        swagger_url = "/docs"
        openapi_url = "/openapi.json"


    async def startup_tasks():
        await scheduler.start()

    async def shutdown_tasks():
        await scheduler.stop()

    application = FastAPI(
        title=config.server.SERVER_NAME,
        description=config.server.SERVER_DESCRIPTION,
        debug=config.server.DEBUG,
        version=config.server.API_VERSION,
        docs_url=swagger_url,
        openapi_url=openapi_url,
        redoc_url=redoc_url,
        responses=config.server.server_responces,
        swagger_ui_parameters=config.server.swagger_ui_parameters,
        on_startup=[bot_manager.run_all, user_service.create_test_user,scheduler.start],
        on_shutdown=[bot_manager.stop_all,scheduler.stop],
    )

    application.middleware("http")(LoggingMiddleware())
    for route in routes:
        application.include_router(route, prefix="/api")

    Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=False,
    ).instrument(application).expose(application, include_in_schema=False)

    return application
@Попов Никита @Шапошникова Диана
я чуть чуть исправил
ваша часть бд
и чтобы разные боты были
Козлов Никита

 — Вчера, в 13:40
Изображение
Изображение
Изображение
Изображение
Вот это сейчас вы делайте
я пока другой хуйнёй занимаюсь
Попов Никита — Вчера, в 14:05
from datetime import datetime
from typing import TYPE_CHECKING
import uuid as uuid_lib
from zoneinfo import ZoneInfo

import sqlalchemy as sa
Раскрыть
notification.py
4 кб
from typing import TYPE_CHECKING
import uuid as uuid_lib

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy.orm as so
Раскрыть
booking.py
2 кб
# app/infrastructure/database/alembic/versions/2026_01_22_1200-notifications_table.py
"""Create notifications table

Revision ID: notifications001
Revises: a4ed92b554b0
Create Date: 2026-01-22 12:00:00.000000
Раскрыть
2026_01_22_1200-notifications_table.py
6 кб
бд
Козлов Никита

 — Вчера, в 17:30
https://github.com/stpnvkirill/booking-management-system/pull/23
GitHub
Notification by x1tle · Pull Request #23 · stpnvkirill/booking-ma...
📌 Цель изменений
Создание надежной системы асинхронных уведомлений для отправки напоминаний о бронированиях через Telegram, обеспечивающей автоматическую фоновую обработку и отслеживание ...
Notification by x1tle · Pull Request #23 · stpnvkirill/booking-ma...
вроде обновился
Козлов Никита

 — 6:28
@Матвей Саширин скинь в тг
Матвей Саширин — 6:34
в чат группы?
Козлов Никита

 — 6:35
Изображение
Нужно это исправь и опубликовать
или похуй мб прокатит
Попов Никита — 6:43
А ты че не сделал что ли вчера
Я думал сделал
Козлов Никита

 — 6:44
да я файл найти не могу бл
Попов Никита — 6:44
Я не понимаю это доеб просто
Точнее вопрос
Козлов Никита

 — 6:45
я тоже не понимаю
Попов Никита — 6:45
Или доеб с намеком на исправление
Козлов Никита

 — 6:45
типо он думает что один бот будет
Попов Никита — 6:45
Че он хочет блять
Козлов Никита

 — 6:45
ну bot_token же через стринг получаем в функции да?
или я ебалн
Попов Никита — 6:45
Ну из конфига стрингом да
А как еще
Козлов Никита

 — 6:45
а нам походу через базу данных получать его хуй знает
там вроде както через бд можно
Попов Никита — 6:46
Щас посмотрю
Козлов Никита

 — 6:46
Изображение
https://github.com/stpnvkirill/booking-management-system/blob/Notification/app/infrastructure/database/models/users.py
GitHub
booking-management-system/app/infrastructure/database/models/users....
Проект для практики. Contribute to stpnvkirill/booking-management-system development by creating an account on GitHub.
booking-management-system/app/infrastructure/database/models/users....
Да сука
он в бд
я щас визуалку новую скачаю
эта мозги ебёт
пока поделай без меня
там хули строчку изменить
Попов Никита — 6:47
Ща
Попов Никита — 7:11
@Козлов Никита
import asyncio
from datetime import datetime, timedelta
import logging
from typing import Any
from zoneinfo import ZoneInfo
Раскрыть
message.txt
12 кб
scheduler.py это
елси че в тг пиши
﻿
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
