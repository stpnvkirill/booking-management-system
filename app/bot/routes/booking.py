# ruff: noqa: DTZ007, DTZ011, RUF001, RUF002, RUF003, RUF006

import asyncio
from datetime import date, datetime, timedelta

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.bot.booking_store import auto_confirm, format_booking, store
from app.bot.fsm.booking_states import BookingStates
from app.bot.keyboards.main_menu import (
    get_confirm_inline,
    get_date_inline,
    get_main_menu,
    get_resource_type_inline,
    get_resources_inline,
    get_success_inline,
    get_time_inline,
)

router = Router()

TYPE_MAP = {
    "meeting": {
        "label": "🏢 Переговорная",
        "resources": ["Переговорка #1", "Переговорка #2", "Переговорка #3"],
    },
    "workspace": {
        "label": "💻 Рабочее место",
        "resources": ["Рабочее место #1", "Рабочее место #2", "Рабочее место #3"],
    },
}


SLOTS = ["10:00 – 10:30", "10:30 – 11:00", "11:00 – 11:30"]


def get_today() -> date:  # получение сегодняшней даты
    return date.today()


def parse_date(text: str) -> date | None:
    "Парсим дату в формате ДД.ММ.ГГГГ."
    try:
        return datetime.strptime(text, "%d.%m.%Y").date()
    except ValueError:
        return None


def validate_slot(text: str) -> bool:  
    return text in SLOTS


def validate_date(
    selected: date,
) -> bool:  # проверка даты не в прошлом и возврат в bool
    return selected >= get_today()


def get_state_summary(data: dict) -> str:
    return (
        "Проверьте детали бронирования 👇\n\n"
        f"🏢 Ресурс: {data.get('selected_resource')}\n"
        f"📅 Дата: {data.get('selected_date')}\n"
        f"⏰ Время: {data.get('selected_time')}"
    )


def get_booking_router():
    return router


@router.message(F.text.contains("Забронировать"))
async def start_booking(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(BookingStates.resource_type)
    await message.answer(
        "Отлично! Что вы хотите забронировать?",
        reply_markup=get_resource_type_inline(),
    )


@router.callback_query(F.data.startswith("type:"))
async def choose_resource_type(callback: CallbackQuery, state: FSMContext):
    type_code = callback.data.split(":", 1)[1]
    type_info = TYPE_MAP.get(type_code)
    if not type_info:
        await callback.answer("Неверный тип.", show_alert=True)
        return
    await state.update_data(
        selected_type_code=type_code,
        selected_resource_type=type_info["label"],
    )
    await state.set_state(BookingStates.resource)
    busy_resources = store.get_busy_resources(type_info["label"])
    await callback.message.edit_text(
        "Выберите конкретный ресурс:",
        reply_markup=get_resources_inline(
            type_info["resources"],
            busy=busy_resources,
        ),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("resource:"))
async def choose_resource(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    type_code = data.get("selected_type_code")
    type_label = data.get("selected_resource_type")
    if not type_code or not type_label:
        await callback.answer("Тип не выбран. Начните заново.", show_alert=True)
        return
    resources = TYPE_MAP.get(type_code, {}).get("resources", [])
    try:
        idx = int(callback.data.split(":", 1)[1]) - 1
    except ValueError:
        await callback.answer("Некорректный ресурс.", show_alert=True)
        return
    if idx < 0 or idx >= len(resources):
        await callback.answer("Ресурс не найден.", show_alert=True)
        return
    selected_resource = resources[idx]
    busy_resources = store.get_busy_resources(type_label)
    if selected_resource in busy_resources:
        await callback.answer("Ресурс занят, выберите другой.", show_alert=True)
        return
    await state.update_data(selected_resource=selected_resource)
    await state.set_state(BookingStates.date)
    await callback.message.edit_text(
        "На какую дату вы хотите забронировать?",
        reply_markup=get_date_inline(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("date:"))
async def choose_date(callback: CallbackQuery, state: FSMContext):
    code = callback.data.split(":", 1)[1]
    if code == "today":
        selected_date = "Сегодня"
    elif code == "tomorrow":
        selected_date = "Завтра"
    else:
        await callback.answer("Некорректная дата.", show_alert=True)
        return

    await state.update_data(selected_date=selected_date)
    await state.set_state(BookingStates.time)
    await callback.message.edit_text(
        "Выберите удобное время:",
        reply_markup=get_time_inline(SLOTS),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("time:"))
async def choose_time(callback: CallbackQuery, state: FSMContext):
    slot = callback.data.split(":", 1)[1]
    if not validate_slot(slot):
        await callback.answer("Некорректный слот.", show_alert=True)
        return
    await state.update_data(selected_time=slot)
    data = await state.get_data()
    await state.set_state(BookingStates.confirm)
    await callback.message.edit_text(
        get_state_summary(data),
        reply_markup=get_confirm_inline(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("confirm:"))
async def confirm_booking(callback: CallbackQuery, state: FSMContext):
    decision = callback.data.split(":", 1)[1]
    if decision == "no":
        await state.clear()
        await callback.message.edit_text(
            "❌ Бронирование отменено.\nНадеемся, вы вернётесь к нам снова!",
            reply_markup=get_main_menu(),
        )
        await callback.answer()
        return
    if decision != "yes":
        await callback.answer("Некорректное действие.", show_alert=True)
        return

    data = await state.get_data()
    await state.clear()
    booking = store.add_booking(
        user_id=callback.from_user.id,
        payload={
            "resource_type": data.get("selected_resource_type"),
            "resource": data.get("selected_resource"),
            "date": data.get("selected_date"),
            "time": data.get("selected_time"),
        },
    )

    await callback.message.edit_text(
        "✅ Готово! Ваша бронь успешно создана.\n"
        "Мы напомним вам перед началом 👍\n\n"
        + format_booking(booking),
        reply_markup=get_success_inline(),
    )
    await callback.answer()

    async def notify(updated_booking: dict):
        await callback.message.answer(
            "Статус обновлён:\n" + format_booking(updated_booking),
            reply_markup=get_main_menu(),
        )

    asyncio.create_task(
        auto_confirm(callback.from_user.id, booking["id"], delay_sec=3, notify=notify),
    )


@router.callback_query(F.data.startswith("back:"))
async def go_back(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split(":", 1)[1]
    data = await state.get_data()

    if action == "main":
        await state.clear()
        await callback.message.edit_text(
            "Вы вернулись в главное меню",
            reply_markup=get_main_menu(),
        )
        await callback.answer()
        return

    if action == "type":
        await state.set_state(BookingStates.resource_type)
        await callback.message.edit_text(
            "Отлично! Что вы хотите забронировать?",
            reply_markup=get_resource_type_inline(),
        )
        await callback.answer()
        return

    if action == "resource":
        type_code = data.get("selected_type_code")
        type_label = data.get("selected_resource_type")
        if not type_code or not type_label:
            await callback.answer("Тип не выбран.", show_alert=True)
            return
        busy = store.get_busy_resources(type_label)
        await state.set_state(BookingStates.resource)
        await callback.message.edit_text(
            "Выберите конкретный ресурс:",
            reply_markup=get_resources_inline(TYPE_MAP[type_code]["resources"], busy=busy),
        )
        await callback.answer()
        return

    if action == "date":
        await state.set_state(BookingStates.date)
        await callback.message.edit_text(
            "На какую дату вы хотите забронировать?",
            reply_markup=get_date_inline(),
        )
        await callback.answer()
        return

    if action == "time":
        await state.set_state(BookingStates.time)
        await callback.message.edit_text(
            "Выберите удобное время:",
            reply_markup=get_time_inline(SLOTS),
        )
        await callback.answer()
        return

    await callback.answer("Некорректное действие.", show_alert=True)