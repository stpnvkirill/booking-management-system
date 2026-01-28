# ruff: noqa: RUF001
from __future__ import annotations

import contextlib
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from aiogram import Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import sqlalchemy as sa

from app.bot.fsm.booking_states import BookingStates
from app.bot.handler import handler
from app.bot.keyboards.main_menu import get_main_menu
from app.depends import provider
from app.domain.services.bookings import BookingParams, booking_service
from app.infrastructure.database import BotConfig, Resource

if TYPE_CHECKING:
    from uuid import UUID

    from aiogram.fsm.context import FSMContext

    from app.infrastructure.database.models.users import User


# Constants for date/time parsing
MIN_DATE_PARTS = 2
TIME_RANGE_PARTS = 2
DATE_FORMATS = ("%Y-%m-%d", "%d.%m.%Y")
TIME_FORMAT = "%H:%M"


def _main_back_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ В главное меню",
                    callback_data="nav:main",
                ),
            ],
        ],
    )


async def _get_customer_id(bot_id: int) -> UUID:
    bot_cfg = await BotConfig.get(id=bot_id)
    return bot_cfg.owner_id


async def _list_resources(customer_id) -> list[Resource]:
    async with provider.session_factory() as session:
        stmt = (
            sa.select(Resource)
            .where(Resource.customer_id == customer_id)
            .order_by(Resource.name.asc())
        )
        result = await session.scalars(stmt)
        return result.all()


def _resources_inline(resources: list[Resource]) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    for r in resources:
        rows.append(
            [
                InlineKeyboardButton(
                    text=r.name,
                    callback_data=f"book:res:{r.id}",
                ),
            ],
        )
    rows.append(
        [InlineKeyboardButton(text="⬅️ В главное меню", callback_data="nav:main")],
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def _format_dt(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%d.%m.%Y %H:%M UTC")


def _get_status_emoji(is_available: bool) -> str:
    """Return emoji for resource status: green circle if available, red if busy."""
    return "🟢" if is_available else "🔴"


def _parse_period(text: str) -> tuple[datetime, datetime] | None:
    """
    Supported formats (minimal, for bot UX):
    - 2026-01-26 10:00-12:00
    - 26.01.2026 10:00-12:00
    - 2026-01-26 10:00 12:00
    - 26.01.2026 10:00 12:00
    Times are interpreted as UTC if timezone not specified.
    """
    raw = " ".join(text.strip().split())
    if not raw:
        return None

    # Split by space into date + time part(s)
    parts = raw.split(" ")
    if len(parts) < MIN_DATE_PARTS:
        return None
    date_part = parts[0]
    time_part = " ".join(parts[1:])

    # Parse date
    date_obj = None
    for fmt in DATE_FORMATS:
        try:
            date_obj = datetime.strptime(date_part, fmt).date()  # noqa: DTZ007
            break
        except ValueError:
            continue
    if date_obj is None:
        return None

    # Parse times (either "HH:MM-HH:MM" or "HH:MM HH:MM")
    if "-" in time_part:
        t1s, t2s = [s.strip() for s in time_part.split("-", 1)]
    else:
        t_parts = time_part.split(" ")
        if len(t_parts) != TIME_RANGE_PARTS:
            return None
        t1s, t2s = t_parts

    try:
        t1 = datetime.strptime(t1s, TIME_FORMAT).time()  # noqa: DTZ007
        t2 = datetime.strptime(t2s, TIME_FORMAT).time()  # noqa: DTZ007
    except ValueError:
        return None

    start = datetime.combine(date_obj, t1).replace(tzinfo=timezone.utc)
    end = datetime.combine(date_obj, t2).replace(tzinfo=timezone.utc)
    return (start, end)


def get_bookings_router() -> Router:
    router: Router = Router()

    @router.message(lambda m: m.text == "📅 Забронировать")
    @handler
    async def start_booking(message: types.Message, state: FSMContext):
        customer_id = await _get_customer_id(message.bot.id)
        resources = await _list_resources(customer_id)
        if not resources:
            await message.answer(
                "Пока нет доступных ресурсов для бронирования.",
                reply_markup=get_main_menu(),
            )
            return
        await state.clear()
        await message.answer(
            "Выберите ресурс для бронирования:",
            reply_markup=_resources_inline(resources),
        )

    @router.callback_query(lambda c: c.data and c.data.startswith("book:res:"))
    @handler
    async def pick_resource(
        callback: types.CallbackQuery,
        state: FSMContext,
    ):
        _, _, resource_id_str = callback.data.split(":", 2)
        try:
            resource_id = int(resource_id_str)
        except ValueError:
            await callback.answer("Некорректный ресурс")
            return

        customer_id = await _get_customer_id(callback.bot.id)
        resource = await Resource.get(id=resource_id)
        if not resource or resource.customer_id != customer_id:
            await callback.answer("Ресурс не найден")
            return

        await state.update_data(resource_id=resource_id)
        await state.set_state(BookingStates.time)
        await callback.message.edit_text(
            f"Выбран ресурс: *{resource.name}*\n\n"
            "Введите дату и время в формате:\n"
            "`26.01.2026 10:00-12:00`\n"
            "или\n"
            "`2026-01-26 10:00-12:00`",
            parse_mode="Markdown",
            reply_markup=_main_back_inline(),
        )
        await callback.answer()

    @router.message(BookingStates.time)
    @handler
    async def receive_period(message: types.Message, state: FSMContext, user: User):
        data = await state.get_data()
        resource_id = data.get("resource_id")
        if not resource_id:
            await state.clear()
            await message.answer(
                "Начните заново: нажмите «📅 Забронировать».",
                reply_markup=get_main_menu(),
            )
            return

        parsed = _parse_period(message.text or "")
        if not parsed:
            await message.answer(
                "Не понял формат. Пример: `26.01.2026 10:00-12:00`",
                parse_mode="Markdown",
            )
            return
        start_time, end_time = parsed

        customer_id = await _get_customer_id(message.bot.id)

        # Check availability
        is_available = await booking_service.check_availability(
            resource_id=int(resource_id),
            start_time=start_time,
            end_time=end_time,
        )

        if not is_available:
            status_emoji = _get_status_emoji(False)
            await message.answer(
                f"{status_emoji} *Ресурс занят на выбранное время*\n\n"
                f"Интервал: {_format_dt(start_time)} – {_format_dt(end_time)}\n\n"
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
        status_emoji = _get_status_emoji(True)
        await message.answer(
            f"{status_emoji} *Бронирование успешно создано!*\n\n"
            f"- Ресурс: `{params.resource_id}`\n"
            f"- С: {_format_dt(params.start_time)}\n"
            f"- По: {_format_dt(params.end_time)}",
            parse_mode="Markdown",
            reply_markup=get_main_menu(),
        )

    @router.message(lambda m: m.text == "🗓 Мои бронирования")
    @handler
    async def my_bookings(message: types.Message, state: FSMContext, user: User):
        await state.clear()
        customer_id = await _get_customer_id(message.bot.id)
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
            status_emoji = _get_status_emoji(True)
            title = (
                f"{status_emoji} #{b.id} · {resource_name} · {_format_dt(b.start_time)}"
            )
            rows.append(
                [InlineKeyboardButton(text=title, callback_data=f"mybook:show:{b.id}")],
            )
        rows.append(
            [InlineKeyboardButton(text="⬅️ В главное меню", callback_data="nav:main")],
        )

        await message.answer(
            "Ваши бронирования:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
        )

    @router.callback_query(lambda c: c.data and c.data.startswith("mybook:show:"))
    @handler
    async def show_booking(callback: types.CallbackQuery, user: User):
        _, _, booking_id_str = callback.data.split(":", 2)
        try:
            booking_id = int(booking_id_str)
        except ValueError:
            await callback.answer("Некорректный ID")
            return

        customer_id = await _get_customer_id(callback.bot.id)
        bookings = await booking_service.get_user_bookings(
            user_id=user.id,
            customer_id=customer_id,
        )
        booking = next((b for b in bookings if b.id == booking_id), None)
        if not booking:
            await callback.answer("Бронирование не найдено")
            return

        resource = await Resource.get(id=booking.resource_id)
        status_emoji = _get_status_emoji(True)
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="❌ Отменить",
                        callback_data=f"mybook:cancel:{booking.id}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️ Назад к списку",
                        callback_data="mybook:list",
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
            f"- С: {_format_dt(booking.start_time)}\n"
            f"- По: {_format_dt(booking.end_time)}",
            parse_mode="Markdown",
            reply_markup=kb,
        )
        await callback.answer()

    @router.callback_query(lambda c: c.data == "mybook:list")
    @handler
    async def back_to_list(callback: types.CallbackQuery, user: User):
        customer_id = await _get_customer_id(callback.bot.id)
        bookings = await booking_service.get_user_bookings(
            user_id=user.id,
            customer_id=customer_id,
        )
        if not bookings:
            await callback.message.edit_text(
                "У вас пока нет бронирований.",
                reply_markup=_main_back_inline(),
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
            status_emoji = _get_status_emoji(True)
            title = (
                f"{status_emoji} #{b.id} · {resource_name} · {_format_dt(b.start_time)}"
            )
            rows.append(
                [InlineKeyboardButton(text=title, callback_data=f"mybook:show:{b.id}")],
            )
        rows.append(
            [InlineKeyboardButton(text="⬅️ В главное меню", callback_data="nav:main")],
        )
        await callback.message.edit_text(
            "Ваши бронирования:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
        )
        await callback.answer()

    @router.callback_query(lambda c: c.data and c.data.startswith("mybook:cancel:"))
    @handler
    async def cancel_booking(callback: types.CallbackQuery, user: User):
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
            reply_markup=_main_back_inline(),
        )
        await callback.answer()

    @router.callback_query(lambda c: c.data == "nav:main")
    @handler
    async def nav_main(callback: types.CallbackQuery, state: FSMContext):
        await state.clear()
        await callback.message.answer("Главное меню:", reply_markup=get_main_menu())
        with contextlib.suppress(Exception):
            await callback.message.delete()
        await callback.answer()

    return router
