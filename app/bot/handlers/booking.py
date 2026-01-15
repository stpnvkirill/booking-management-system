import asyncio
from datetime import date, datetime, timedelta

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.bot.booking_store import auto_confirm, format_booking, store
from app.bot.fsm.booking_states import BookingStates
from app.bot.keyboards import (
    get_confirm_keyboard,
    get_date_keyboard,
    get_main_menu,
    get_resource_type_keyboard,
    get_resources_keyboard,
    get_time_keyboard,
)

router = Router()

RESOURCE_MAP = {
    "🏨 Отель": ["Отель Альфа", "Отель Бета"],
    "🏠 Квартира": ["Квартира Центр", "Квартира Парк"],
}


def get_slots(
    start: str = "09:00", end: str = "18:00",
) -> list[str]:  # получение слотов времени
    start_dt = datetime.strptime(start, "%H:%M")
    end_dt = datetime.strptime(end, "%H:%M")
    slots: list[str] = []
    current = start_dt
    while current <= end_dt:
        slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=30)
    return slots


SLOTS = get_slots()  # список слотов времени с шагом 30 минут


def get_today() -> date:  # получение сегодняшней даты
    return date.today()


def parse_date(text: str) -> date | None:
    "Парсим дату в формате ДД.ММ.ГГГГ."
    try:
        return datetime.strptime(text, "%d.%m.%Y").date()
    except ValueError:
        return None


def validate_slot(text: str) -> bool:  # валидация слотов времени в bool
    return text in SLOTS


def validate_date(
    selected: date,
) -> bool:  # проверка даты не в прошлом и возврат в bool
    return selected >= get_today()


def get_state_summary(data: dict) -> str:  # получение сводки состояния бронирования
    return (
        f"Тип: {data.get('selected_resource_type')}\n"
        f"Ресурс: {data.get('selected_resource')}\n"
        f"Дата: {data.get('selected_date')}\n"
        f"Время: {data.get('selected_time')}"
    )


def get_booking_router():
    return router


@router.message(lambda m: m.text == "📅 Забронировать")
async def start_booking(message: Message, state: FSMContext):
    await state.set_state(
        BookingStates.resource_type,
    )  # установка состояния выбора типа ресурса
    await message.answer(
        "Отлично! Что вы хотите забронировать?:",
        reply_markup=get_resource_type_keyboard(),  # клавиатура выбора типа ресурса
    )


@router.message( BookingStates.resource_type,)  # говорим что мы на этапе выбора типа ресурса
async def choose_resource_type( message: Message, state: FSMContext,):  # получаем на вход сообщение и состояние
    selected_resource_type = message.text  # ввод пользователя
    if selected_resource_type not in RESOURCE_MAP:  # проверяем правильность ввода
        await message.answer(
            "Неверный тип. Выберите из списка.",
            reply_markup=get_resource_type_keyboard(),
        )
        return
    await state.update_data(selected_resource_type=selected_resource_type, )  # сохраняем выбранный тип ресурса
    await state.set_state(BookingStates.resource, )  # переходим к следующему состоянию - выбор конкретного ресурса
    busy_resources = store.get_busy_resources(selected_resource_type)
    await message.answer(  # пишем ответ пользователю
        f"Вы выбрали: {selected_resource_type}\nТеперь выберите ресурс:",
        reply_markup=get_resources_keyboard(RESOURCE_MAP[selected_resource_type], busy=busy_resources),  # открываем клавиатуру с конкретными ресурсами и статусом занятости
    )


@router.message(BookingStates.resource)
async def choose_resource(message: Message, state: FSMContext):
    data = await state.get_data()  # получаем данные из состояния в data
    selected_resource_type = data.get(
        "selected_resource_type",  )  # получаем выбранный тип ресурса
    available_resources = RESOURCE_MAP.get( selected_resource_type, [], )  # получаем доступные ресурсы для выбранного типа
    busy_resources = store.get_busy_resources(selected_resource_type)
    selected_resource_text = (
        message.text.replace("🔴 ", "").replace("🟢 ", "") )  # получаем ввод пользователя
    if selected_resource_text not in available_resources:  # проверяем правильность ввода
        await message.answer(
            "Неверный ресурс. Выберите из списка.",
            reply_markup=get_resources_keyboard(available_resources, busy=busy_resources, ),
        )
        return
    if selected_resource_text in busy_resources:
        await message.answer(
            "Ресурс занят. Выберите другой.",
            reply_markup=get_resources_keyboard(
                available_resources, busy=busy_resources,
            ),
        )
        return
    await state.update_data(
        selected_resource=selected_resource_text,
    )  # сохраняем выбранный ресурс в состояние selected_resource
    await state.set_state(
        BookingStates.date,
    )  # переходим к следующему состоянию - выбор даты
    await message.answer(  # пишем ответ пользователю
        "Выберите дату: сегодня/завтра или введите в формате ДД.ММ.ГГГГ",
        reply_markup=get_date_keyboard(),  # открываем клавиатуру выбора даты
    )


@router.message(BookingStates.date)
async def choose_date(message: Message, state: FSMContext):
    text = message.text
    if text == "Сегодня":
        selected = get_today()
    elif text == "Завтра":
        selected = get_today() + timedelta(days=1)
    elif text == "Ввести дату":
        await message.answer("Введите дату в формате ДД.ММ.ГГГГ (не раньше сегодня)")
        return
    else:
        selected = parse_date(text)
        if selected is None:
            await message.answer("Неверный формат даты. Используйте ДД.ММ.ГГГГ.")
            return

    if not validate_date(selected):
        await message.answer("Дата не может быть в прошлом. Выберите другую.")
        return

    await state.update_data(selected_date=selected.strftime("%d.%m.%Y"))
    await state.set_state(BookingStates.time)
    await message.answer(
        "Выберите время (шаг 30 минут):",
        reply_markup=get_time_keyboard(SLOTS),
    )


@router.message(BookingStates.time)
async def choose_time(message: Message, state: FSMContext):
    selected_time_slot = message.text
    if not validate_slot(selected_time_slot):
        await message.answer(
            "Неверный слот. Выберите из клавиатуры.",
            reply_markup=get_time_keyboard(SLOTS),
        )
        return
    await state.update_data(selected_time=selected_time_slot)
    data = await state.get_data()
    await state.set_state(BookingStates.confirm)
    await message.answer(
        "Проверьте данные:\n" + get_state_summary(data),
        reply_markup=get_confirm_keyboard(),
    )


@router.message(BookingStates.confirm)
async def confirm_booking(message: Message, state: FSMContext):
    text = message.text
    if text == "❌ Отменить":
        await state.clear()
        await message.answer("Бронирование отменено.", reply_markup=get_main_menu())
        return
    if text != "✅ Подтвердить":
        await message.answer(
            "Нажмите Подтвердить или Отменить.", reply_markup=get_confirm_keyboard(),
        )
        return

    data = await state.get_data()
    await state.clear()
    booking = store.add_booking(
        user_id=message.from_user.id,
        payload={
            "resource_type": data.get("selected_resource_type"),
            "resource": data.get("selected_resource"),
            "date": data.get("selected_date"),
            "time": data.get("selected_time"),
        },
    )

    await message.answer(
        "Бронь создана (pending):\n" + format_booking(booking),
    )

    async def notify(updated_booking: dict):
        await message.answer(
            "Статус обновлён:\n" + format_booking(updated_booking),
            reply_markup=get_main_menu(),
        )

    # Имитация фонового подтверждения
    asyncio.create_task(
        auto_confirm(message.from_user.id, booking["id"], delay_sec=3, notify=notify),
    )
