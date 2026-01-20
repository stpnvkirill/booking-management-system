# ruff: noqa: RUF001

from aiogram import F, Router
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

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


def get_cancel_confirm_keyboard(booking_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить отмену",
                    callback_data=f"confirm_cancel:{booking_id}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="↩️ Оставить без изменений",
                    callback_data="cancel_cancel",
                ),
            ],
        ],
    )


def get_mybooking_router():
    return router


@router.message(lambda m: m.text in {"🗓 Мои бронирования", "🗓️ Мои бронирования"})
async def list_bookings(message: Message):
    bookings = store.list_bookings(message.from_user.id)
    if not bookings:
        await message.answer(
            "У вас пока нет броней.",
            reply_markup=get_backbutton_keyboard(),
        )
        return
    text = "📋 Ваши активные бронирования:\n\n" + "\n\n".join(
        format_booking(b) for b in bookings
    )
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
    booking = next(
        (
            b
            for b in store.list_bookings(callback.from_user.id)
            if b["id"] == booking_id
        ),
        None,
    )
    if not booking:
        await callback.answer("Бронь не найдена.", show_alert=True)
        return
    if booking.get("status") == "cancelled":
        await callback.answer("Бронь уже отменена.", show_alert=True)
        return
    await callback.answer()
    await callback.message.answer(
        "Подтвердите отмену бронирования:\n" + format_booking(booking),
        reply_markup=get_cancel_confirm_keyboard(booking_id),
    )


@router.callback_query(F.data.startswith("confirm_cancel:"))
async def confirm_cancel_booking(callback: CallbackQuery):
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


@router.callback_query(F.data == "cancel_cancel")
async def cancel_cancel(callback: CallbackQuery):
    await callback.answer("Отмена бронирования не подтверждена.")
