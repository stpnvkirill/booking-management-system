from aiogram import Router
from aiogram.types import Message

from app.bot.keyboards.main_menu import get_main_menu

router = Router()


async def echo_handler(message: Message):
    await message.answer(
        f"Не знаю что вам ответить: {message.from_user.id}",
        reply_markup=get_main_menu(),
    )


def get_echo_router():
    router.message.register(echo_handler)
    return router
