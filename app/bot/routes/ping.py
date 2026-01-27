from aiogram import Router, types
from aiogram.filters import command
from app.bot.handler import handler
import sqlalchemy as sa

from app.depends import provider


def get_ping_router() -> Router:
    router: Router = Router()

    @router.message(command.Command("ping"))
    @handler
    async def process_ping(message: types.Message):
        async with provider.session_factory() as session:
            stmt = sa.text(
                "SELECT substring(md5(random()::text) from 1 for 10) as random_string;",
            )
            random_string = await session.scalar(stmt)
        await message.reply(text=random_string)

    return router
