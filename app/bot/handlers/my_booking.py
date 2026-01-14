from aiogram import Router
from aiogram.types import Message

from app.bot.booking_store import format_booking, store
from app.bot.keyboards.main_menu import get_backbutton_keyboard

router = Router()


def get_mybooking_router():
    return router


@router.message(lambda m: m.text == "🗓️ Мои бронирования")
async def list_bookings(message: Message):
    bookings = store.list_bookings(message.from_user.id)
    if not bookings:
        await message.answer(
            "У вас пока нет броней.",
            reply_markup=get_backbutton_keyboard(),
        )
        return
    text = "Ваши бронирования:\n\n" + "\n\n".join(format_booking(b) for b in bookings)
    await message.answer(text, reply_markup=get_backbutton_keyboard())
