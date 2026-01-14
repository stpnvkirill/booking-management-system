from aiogram import Router
from aiogram.types import Message

from app.bot.keyboards.main_menu import get_backbutton_keyboard

router = Router()


def get_reviews_router():
    return router


def post_reviews_database():
    # логика отправки в бд
    pass


@router.message(lambda m: m.text == "⭐ Оставить отзыв")
async def start_reviews(message: Message):
    await message.answer("Оставьте отзыв: ", reply_markup=get_backbutton_keyboard())
