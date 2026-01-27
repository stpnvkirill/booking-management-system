from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from app.bot.handler import handler

from app.bot.keyboards.main_menu import get_main_menu


def get_reviews_router() -> Router:
    router: Router = Router()

    @router.message(lambda m: m.text == "⭐️ Оставить отзыв")
    @handler
    async def start_reviews(message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer(
            "Функция отзывов временно недоступна. ",
            reply_markup=get_main_menu(),
        )

    return router
