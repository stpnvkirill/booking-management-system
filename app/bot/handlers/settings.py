from aiogram import Router
from aiogram.types import Message

from app.bot.keyboards.main_menu import get_settings_keyboard

router = Router()


def get_settings_router():
    return router


@router.message(lambda m: m.text == "⚙️ Настройки")
async def start_reviews(message: Message):
    await message.answer("Выберите настройки: ", reply_markup=get_settings_keyboard())
