# ruff: noqa: RUF001, PLR0915
"""Handlers for viewing and managing bookings."""

from typing import TYPE_CHECKING

from aiogram import Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.handler import handler
from app.bot.keyboards.main_menu import get_main_menu
from app.domain.services.bookings import booking_service
from app.infrastructure.database import Resource

from .helpers import format_dt, get_customer_id, get_status_emoji, main_back_inline

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext

    from app.infrastructure.database.models.users import User


def get_list_router() -> Router:
    """Create router for booking list handlers."""
    router = Router()

    @router.message(lambda m: m.text == "🗓 Мои бронирования")
    @handler
    async def my_bookings(message: types.Message, state: FSMContext, user: User):
        """Show list of user bookings."""
        await state.clear()
        customer_id = await get_customer_id(message.bot.id)
        bookings = await booking_service.get_user_bookings(
            user_id=user.id,
            customer_id=customer_id,
        )
        if not bookings:
            await message.answer(
                "У вас пока нет бронирований.",
                reply_markup=get_main_menu(),
            )
            return

        resource_ids = sorted({b.resource_id for b in bookings})
        resources = await Resource.get_by_id_list(id_list=resource_ids)
        resource_name_by_id = {r.id: r.name for r in resources}

        rows: list[list[InlineKeyboardButton]] = []
        for b in bookings:
            resource_name = resource_name_by_id.get(
                b.resource_id,
                f"ресурс {b.resource_id}",
            )
            status_emoji = get_status_emoji(True)
            title = (
                f"{status_emoji} #{b.id} · {resource_name} · {format_dt(b.start_time)}"
            )
            rows.append(
                [InlineKeyboardButton(text=title, callback_data=f"booking:show:{b.id}")],
            )
        rows.append(
            [InlineKeyboardButton(text="⬅️ В главное меню", callback_data="nav:main")],
        )

        await message.answer(
            "Ваши бронирования:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
        )

    @router.callback_query(lambda c: c.data and c.data.startswith("booking:show:"))
    @handler
    async def show_booking(callback: types.CallbackQuery, user: User):
        """Show details of a single booking."""
        _, _, booking_id_str = callback.data.split(":", 2)
        try:
            booking_id = int(booking_id_str)
        except ValueError:
            await callback.answer("Некорректный ID")
            return

        customer_id = await get_customer_id(callback.bot.id)
        bookings = await booking_service.get_user_bookings(
            user_id=user.id,
            customer_id=customer_id,
        )
        booking = next((b for b in bookings if b.id == booking_id), None)
        if not booking:
            await callback.answer("Бронирование не найдено")
            return

        resource = await Resource.get(id=booking.resource_id)
        status_emoji = get_status_emoji(True)
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="❌ Отменить",
                        callback_data=f"booking:cancel:{booking.id}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️ Назад к списку",
                        callback_data="booking:list",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️ В главное меню",
                        callback_data="nav:main",
                    ),
                ],
            ],
        )
        await callback.message.edit_text(
            f"{status_emoji} *Ваше бронирование*\n\n"
            f"- ID: `{booking.id}`\n"
            f"- Ресурс: {resource.name if resource else booking.resource_id}\n"
            f"- С: {format_dt(booking.start_time)}\n"
            f"- По: {format_dt(booking.end_time)}",
            parse_mode="Markdown",
            reply_markup=kb,
        )
        await callback.answer()

    @router.callback_query(lambda c: c.data == "booking:list")
    @handler
    async def back_to_list(callback: types.CallbackQuery, user: User):
        """Return to bookings list."""
        customer_id = await get_customer_id(callback.bot.id)
        bookings = await booking_service.get_user_bookings(
            user_id=user.id,
            customer_id=customer_id,
        )
        if not bookings:
            await callback.message.edit_text(
                "У вас пока нет бронирований.",
                reply_markup=main_back_inline(),
            )
            await callback.answer()
            return

        resource_ids = sorted({b.resource_id for b in bookings})
        resources = await Resource.get_by_id_list(id_list=resource_ids)
        resource_name_by_id = {r.id: r.name for r in resources}

        rows: list[list[InlineKeyboardButton]] = []
        for b in bookings:
            resource_name = resource_name_by_id.get(
                b.resource_id,
                f"ресурс {b.resource_id}",
            )
            status_emoji = get_status_emoji(True)
            title = (
                f"{status_emoji} #{b.id} · {resource_name} · {format_dt(b.start_time)}"
            )
            rows.append(
                [InlineKeyboardButton(text=title, callback_data=f"booking:show:{b.id}")],
            )
        rows.append(
            [InlineKeyboardButton(text="⬅️ В главное меню", callback_data="nav:main")],
        )
        await callback.message.edit_text(
            "Ваши бронирования:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
        )
        await callback.answer()

    @router.callback_query(lambda c: c.data and c.data.startswith("booking:cancel:"))
    @handler
    async def cancel_booking(callback: types.CallbackQuery, user: User):
        """Cancel a booking."""
        _, _, booking_id_str = callback.data.split(":", 2)
        try:
            booking_id = int(booking_id_str)
        except ValueError:
            await callback.answer("Некорректный ID")
            return

        ok = await booking_service.cancel_booking(
            booking_id=booking_id,
            user_id=user.id,
        )
        if not ok:
            await callback.answer("Не удалось отменить")
            return
        await callback.message.edit_text(
            "Бронирование отменено.",
            reply_markup=main_back_inline(),
        )
        await callback.answer()

    return router




