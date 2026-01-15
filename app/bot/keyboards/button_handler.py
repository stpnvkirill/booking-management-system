from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.bot.keyboards.main_menu import get_main_menu

router = Router()


def get_button_handler_router():
    return router


@router.message(lambda m: m.text == "◀️ Назад")
async def back_button(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы вернулись в главное меню", reply_markup=get_main_menu())