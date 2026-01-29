from aiogram import Router, types
from aiogram.filters import Command

from . import keyboards


def get_admin_handlers_router() -> Router:
    router = Router()

    @router.message(Command(commands=["start", "menu"]))
    async def cmd_start(message: types.Message):
        await message.answer(
            "Добро пожаловать в админ панель! Выберите действие:",
            reply_markup=keyboards.main_menu(),
        )

    return router
