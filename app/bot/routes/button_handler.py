from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.bot.keyboards.main_menu import get_main_menu


def get_backbutton_router() -> Router:
    router: Router = Router()

    @router.message(lambda m: m.text == "◀️ Назад")
    async def back_button(message: Message, state: FSMContext):
        await state.clear()
        await message.answer(
            "Вы вернулись в главное меню",
            reply_markup=get_main_menu(),
        )

    return router
get_main_menu())
