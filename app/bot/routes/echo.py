from aiogram import Router, types
from app.bot.handler import handler

from app.bot.filters import OnlyPrivateChatFilter
from app.infrastructure.database import User


def get_echo_router() -> Router:
    router: Router = Router()

    @router.message(OnlyPrivateChatFilter())
    @handler
    async def process_any_message(message: types.Message, user: User):
        await message.reply(text=f"Не знаю что вам ответить: {user.tlg_id}")  # noqa: RUF001

    return router
