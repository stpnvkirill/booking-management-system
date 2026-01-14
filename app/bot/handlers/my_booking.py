from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.fsm.booking_states import BookingStates
from app.bot.keyboards.main_menu import get_backbutton_keyboard

router = Router()

def get_mybooking_router():
    return router

@router.message(lambda m: m.text == "🗓️ Мои бронирования")
async def start_reviews(message: Message):
    await message.answer(
        "Список моих бронирований: ",
        reply_markup=get_backbutton_keyboard()
    )

