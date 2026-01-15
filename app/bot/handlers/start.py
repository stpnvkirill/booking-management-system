from aiogram import Router
from aiogram.types import Message

from app.bot.keyboards.main_menu import get_main_menu

router = Router()


def get_start_router():
    return router


@router.message()
async def start_handler(message: Message):
    if message.text == "/start":
        await message.answer(
            "👋 Привет!\n"
            "Я помогу тебе забронировать ресурс, посмотреть твои бронирования и управлять настройками.",
            reply_markup=get_main_menu(),
        )
