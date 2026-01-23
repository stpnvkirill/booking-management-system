from aiogram import Router
from aiogram.types import Message
from aiogram.filters import command
from app.bot.handler import handler

from app.bot.filters.chat_type import OnlyPrivateChatFilter
from app.bot.keyboards.main_menu import get_main_menu


def get_start_router() -> Router:
    router: Router = Router()

    @router.message(OnlyPrivateChatFilter(), command.Command("start"))
    @handler
    async def start_handler(message: Message):
        await message.answer(
                "👋 Привет!\n"
                "Я помогу тебе забронировать ресурс, посмотреть твои бронирования и управлять настройками.",
                reply_markup=get_main_menu(),
            )
    
    return router
