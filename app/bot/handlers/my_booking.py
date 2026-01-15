from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from app.bot.booking_store import format_booking, store
from app.bot.keyboards.main_menu import get_backbutton_keyboard

router = Router()


def get_cancel_keyboard(bookings: list[dict]) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f"❌ Отменить: {b['resource']} {b['date']} {b['time']}",
                callback_data=f"cancel_booking:{b['id']}",
            ),
        ]
        for b in bookings
        if b.get("status") != "cancelled"
    ]
    if not buttons:
        return InlineKeyboardMarkup(inline_keyboard=[])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


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
    await message.answer(
        text,
        reply_markup=get_backbutton_keyboard(),
    )
    await message.answer(
        "Выберите бронь для отмены:",
        reply_markup=get_cancel_keyboard(bookings),
    )


@router.callback_query(F.data.startswith("cancel_booking:"))
async def cancel_booking(callback: CallbackQuery):
    booking_id = callback.data.split(":", 1)[1]
    updated = store.set_status(callback.from_user.id, booking_id, "cancelled")
    if not updated:
        await callback.answer("Бронь не найдена или уже отменена.", show_alert=True)
        return
    await callback.answer("Бронь отменена.")
    await callback.message.answer(
        "Статус обновлён:\n" + format_booking(updated),
        reply_markup=get_backbutton_keyboard(),
    )
