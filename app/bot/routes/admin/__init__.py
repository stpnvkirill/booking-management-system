from aiogram import Router, types

from app.bot.filters import OnlyPrivateChatFilter
from app.bot.handler import handler
from app.infrastructure.database import User


def create_admin_router() -> Router:
    router: Router = Router()

    @router.message(OnlyPrivateChatFilter())
    @handler
    async def process_any_message(message: types.Message, user: User):
        await message.reply(text=f"Это админ бот: {user.tlg_id}")

    return router
