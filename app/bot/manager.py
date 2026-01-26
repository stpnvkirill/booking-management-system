import asyncio
import uuid

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage

from app.config import config
from app.infrastructure.database import BotConfig
from app.log import log

from .middlewares import register_middleware


class BotManager:
    def __init__(self):
        self.bots: dict[uuid.UUID, Bot] = {}
        self.tasks: dict[uuid.UUID, asyncio.Task] = {}
        self.runners: set[int] = set()
        self.dispatchers: dict[uuid.UUID, Dispatcher] = {}
        self.storages: dict[uuid.UUID, RedisStorage | MemoryStorage] = {}
        self._starting_bots: set[int] = set()

    def create_storage(self, bot_id: int):
        storage = self.storages.get(bot_id)
        if storage is not None:
            return storage
        if config.bot.USE_REDIS_STORAGE:
            rs = RedisStorage.from_url(
                config.bot.BOT_REDIS_DSN,
                key_builder=DefaultKeyBuilder(
                    prefix=f"fsm:{bot_id}",  # Разделение по боту
                ),
            )
            self.storages[bot_id] = rs
            return rs
        ms = MemoryStorage()
        self.storages[bot_id] = ms
        return ms

    def get_dispatcher(self, bot_id: int) -> Dispatcher:
        exist_dp = self.dispatchers.get(bot_id)
        if exist_dp is not None:
            return exist_dp
        dp: Dispatcher = Dispatcher(storage=self.create_storage(bot_id))

        if bot_id == config.bot.ADMINBOT_ID:
            from .routes import create_admin_router as create_router  # noqa: PLC0415
        else:
            from .routes import create_router  # noqa: PLC0415

        router = create_router()
        dp.include_router(router)
        register_middleware(dp)

        self.dispatchers[bot_id] = dp
        return dp

    async def start_bot(self, bot_id: int, bot_token: str | None = None):
        if bot_id in self._starting_bots:
            return
        if bot_id in self.runners:
            await self.stop_bot(bot_id)

        self._starting_bots.add(bot_id)
        try:
            bot = self.bots.get(bot_id)
            if bot is None:
                if bot_token is None:
                    bot_config = await BotConfig.get(id=bot_id)
                    bot_token = bot_config.token

                bot: Bot = Bot(
                    token=bot_token,
                )
                self.bots[bot_id] = bot

            dp = self.get_dispatcher(bot_id)
            await self.run_bot(bot_id=bot_id, bot=bot, dp=dp)
        finally:
            self._starting_bots.discard(bot_id)

    async def run_bot(self, bot_id: int, bot, dp):
        if bot_id in self.runners:
            return

        if config.bot.USE_WEBHOOK:
            webhook_url = config.bot.webhook_url.format(
                bot_id=bot_id,
            )
            await bot.set_webhook(
                webhook_url,
                allowed_updates=dp.resolve_used_update_types(),
            )
        else:
            if bot_id in self.tasks:
                self.tasks[bot_id].cancel()
                try:
                    await self.tasks[bot_id]
                except asyncio.CancelledError:
                    pass

            task = asyncio.create_task(
                dp.start_polling(
                    bot,
                    polling_timeout=30,
                    handle_signals=False,
                    allowed_updates=dp.resolve_used_update_types(),
                ),
            )
            self.tasks[bot_id] = task

        start_type = " set webhook" if config.bot.USE_WEBHOOK else "start polling"
        self.runners.add(bot_id)
        bot_username = (await bot.get_me()).username
        log(
            level="info",
            method="start_bot",
            path="BotManager",
            bot_id=bot_id,
            bot_username=bot_username,
            text_detail=f"Bot {start_type}",
        )

    async def remove_bot(self, bot_id: int):
        """Удаление бота"""
        if bot_id in self.bots:
            await self.bots[bot_id].session.close()
            del self.bots[bot_id]
        if bot_id in self.dispatchers:
            del self.dispatchers[bot_id]
        self.runners.discard(bot_id)
        self._starting_bots.discard(bot_id)

    async def stop_bot(self, bot_id: int):
        """Остановка конкретного бота"""
        if bot_id not in self.runners:
            return

        bot = self.bots.get(bot_id)
        bot_username = None
        if bot:
            try:
                bot_username = (await bot.get_me()).username
            except Exception:  # noqa: BLE001
                pass

        if config.bot.USE_WEBHOOK:
            if bot:
                await bot.delete_webhook()
        elif bot_id in self.tasks:
            self.tasks[bot_id].cancel()
            try:
                await self.tasks[bot_id]
            except asyncio.CancelledError:
                pass
            del self.tasks[bot_id]

        await self.remove_bot(bot_id)
        stop_type = "delete webhook" if config.bot.USE_WEBHOOK else "stop polling"

        log(
            level="info",
            method="stop_bot",
            path="BotManager",
            bot_id=bot_id,
            bot_username=bot_username,
            text_detail=f"Bot {stop_type}",
        )

    async def run_all(self):
        """Запуск всех ботов из конфига"""
        await self.start_bot(
            config.bot.ADMINBOT_ID,
            bot_token=config.bot.ADMINBOT_TOKEN,
        )

        bot_configs = await BotConfig.get_all()
        for bc in bot_configs:
            await self.start_bot(bc.id)

    async def stop_all(self):
        """Остановка всех ботов из конфига"""
        bot_configs = await BotConfig.get_all()
        for bc in bot_configs:
            await self.stop_bot(bc.id)

    async def feed_update(self, bot_id: uuid.UUID, update):
        dp = self.get_dispatcher(bot_id)
        bot = self.bots.get(bot_id)
        if dp is None or bot is None:
            log(
                level="error",
                method="feed_update",
                path="BotManager",
                url=config.bot.WEBHOOK_URL.format(bot_id=bot_id),
                message=f"Bot or Dispatcher not found for bot_id={bot_id}",
            )
            return None
        return await dp.feed_update(bot, update)

    async def check_bot(self, bot_token: str):
        """Проверка валидности токена бота"""
        test_bot = Bot(token=bot_token)
        me = None
        try:
            me = await test_bot.get_me()
            log(
                level="info",
                method="check_bot",
                path="BotManager",
                bot_id=me.id,
                bot_username=me.username,
                text_detail=f"Bot {me.id} token is valid",
            )
        except Exception:  # noqa: BLE001, S110
            pass
        finally:
            await test_bot.session.close()
        return me

    async def add_bot(
        self,
        bot_token: str,
        owner_id: uuid.UUID,
    ) -> int:
        bot = await self.check_bot(bot_token)
        if not bot:
            return None
        existing_bot = await BotConfig.get(id=bot.id)
        if existing_bot:
            log(
                level="warning",
                method="add_bot",
                path="BotManager",
                bot_id=bot.id,
                bot_username=bot.username,
                text_detail=f"Bot {bot.id} already exists",
            )
            return None
        bot_config = await BotConfig.create(
            id=bot.id,
            token=bot_token,
            username=bot.username,
            name=bot.first_name,
            owner_id=owner_id,
        )
        await self.start_bot(bot_config.id)
        return bot_config.id


bot_manager = BotManager()
