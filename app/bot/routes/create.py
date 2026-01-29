# ruff: noqa: RUF001, PLR0915
"""Handlers for creating bookings."""

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from app.bot.fsm.booking_states import BookingStates
from app.bot.handler import handler
from app.bot.keyboards.main_menu import get_main_menu
from app.domain.services.bookings import BookingParams, booking_service
from app.domain.services.resource import resource_service
from app.infrastructure.database import Resource
from app.infrastructure.database.models.users import User

from .helpers import (
    format_bookings_list,
    format_dt,
    get_customer_id,
    get_status_emoji,
    main_back_inline,
    parse_period,
    resources_inline,
)


def get_create_router() -> Router:
    """Create router for booking creation handlers."""
    router = Router()

    @router.message(lambda m: m.text == "📅 Забронировать")
    @handler
    async def start_booking(message: types.Message, state: FSMContext, user: User):
        """Start booking process - show list of resources."""
        customer_id = await get_customer_id(message.bot.id)
        resources = await resource_service.get_resources_for_customer(
            current_user=user,
            customer_id=customer_id,
        )
        if not resources:
            await message.answer(
                "Пока нет доступных ресурсов для бронирования.",
                reply_markup=get_main_menu(),
            )
            return
        await state.clear()
        await message.answer(
            "Выберите ресурс для бронирования:",
            reply_markup=resources_inline(resources),
        )

    @router.callback_query(lambda c: c.data and c.data.startswith("booking:resource:"))
    @handler
    async def pick_resource(
        callback: types.CallbackQuery,
        state: FSMContext,
    ):
        """Handle resource selection."""
        _, _, resource_id_str = callback.data.split(":", 2)
        try:
            resource_id = int(resource_id_str)
        except ValueError:
            await callback.answer("Некорректный ресурс")
            return

        customer_id = await get_customer_id(callback.bot.id)
        resource = await Resource.get(id=resource_id)
        if not resource or resource.customer_id != customer_id:
            await callback.answer("Ресурс не найден")
            return

        # Get existing bookings for this resource
        existing_bookings = await booking_service.get_resource_bookings(
            resource_id=resource_id,
        )
        bookings_text = format_bookings_list(existing_bookings)

        await state.update_data(resource_id=resource_id)
        await state.set_state(BookingStates.time)
        await callback.message.edit_text(
            f"Выбран ресурс: *{resource.name}*\n\n"
            f"{bookings_text}\n\n"
            "Введите дату и время в формате:\n"
            "`26.01.2026 10:00-12:00`\n"
            "или\n"
            "`2026-01-26 10:00-12:00`",
            parse_mode="Markdown",
            reply_markup=main_back_inline(),
        )
        await callback.answer()

    @router.message(BookingStates.time)
    @handler
    async def receive_period(message: types.Message, state: FSMContext, user: User):
        """Handle time period input and create booking."""
        data = await state.get_data()
        resource_id = data.get("resource_id")
        if not resource_id:
            await state.clear()
            await message.answer(
                "Начните заново: нажмите «📅 Забронировать».",
                reply_markup=get_main_menu(),
            )
            return

        parsed = parse_period(message.text or "")
        if not parsed:
            await message.answer(
                "Не понял формат. Пример: `26.01.2026 10:00-12:00`",
                parse_mode="Markdown",
            )
            return
        start_time, end_time = parsed

        customer_id = await get_customer_id(message.bot.id)

        # Check availability
        is_available = await booking_service.check_availability(
            resource_id=int(resource_id),
            start_time=start_time,
            end_time=end_time,
        )

        if not is_available:
            # Get existing bookings to show what's already booked
            existing_bookings = await booking_service.get_resource_bookings(
                resource_id=int(resource_id),
            )
            bookings_text = format_bookings_list(existing_bookings)

            status_emoji = get_status_emoji(False)
            await message.answer(
                f"{status_emoji} *Ресурс занят на выбранное время*\n\n"
                f"Интервал: {format_dt(start_time)} – {format_dt(end_time)}\n\n"
                f"{bookings_text}\n\n"
                "Попробуйте выбрать другой день или время.",
                parse_mode="Markdown",
            )
            return

        params = BookingParams(
            user_id=user.id,
            customer_id=customer_id,
            resource_id=int(resource_id),
            start_time=start_time,
            end_time=end_time,
        )
        booking = await booking_service.create_booking(params=params)
        if not booking:
            msg = (
                "Не удалось создать бронирование "
                "(время занято или введены некорректные даты). "
                "Попробуйте другой интервал."
            )
            await message.answer(msg)
            return

        await state.clear()
        status_emoji = get_status_emoji(True)
        await message.answer(
            f"{status_emoji} *Бронирование успешно создано!*\n\n"
            f"- Ресурс: `{params.resource_id}`\n"
            f"- С: {format_dt(params.start_time)}\n"
            f"- По: {format_dt(params.end_time)}",
            parse_mode="Markdown",
            reply_markup=get_main_menu(),
        )

    return router
