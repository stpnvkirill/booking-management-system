from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


RESOURCE_TYPE_BUTTONS = [
    "🏨 Отель",
    "🏠 Квартира",
]


def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗓️ Мои бронирования")],
            [KeyboardButton(text="📅 Забронировать")],
            [KeyboardButton(text="⭐ Оставить отзыв")],
            [KeyboardButton(text="⚙️ Настройки")],
        ],
        resize_keyboard=True,
    )


def get_resource_type_keyboard() -> ReplyKeyboardMarkup:
    "Клавиатура для выбора типа ресурса"
    rows = [[KeyboardButton(text=btn)] for btn in RESOURCE_TYPE_BUTTONS]
    rows.append([KeyboardButton(text="◀️ Назад")])
    return ReplyKeyboardMarkup(
        keyboard=rows,
        resize_keyboard=True,
    )


def get_resources_keyboard(resources: list[str]) -> ReplyKeyboardMarkup:
    "Клавиатура для выбора конкретного ресурса"
    rows = [[KeyboardButton(text=resource)] for resource in resources]
    rows.append([KeyboardButton(text="◀️ Назад")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def get_date_keyboard() -> ReplyKeyboardMarkup:
    "Клавиатура для выбора даты"
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Сегодня"), KeyboardButton(text="Завтра")],
            [KeyboardButton(text="Ввести дату")],
            [KeyboardButton(text="◀️ Назад")],
        ],
        resize_keyboard=True,
    )


def get_time_keyboard(slots: list[str]) -> ReplyKeyboardMarkup:
    "Клавиатура для выбора времени (слоты)"
    rows: list[list[KeyboardButton]] = []
    step = 3
    for i in range(0, len(slots), step):
        chunk = slots[i : i + step]
        rows.append([KeyboardButton(text=slot) for slot in chunk])
    rows.append([KeyboardButton(text="◀️ Назад")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def get_confirm_keyboard() -> ReplyKeyboardMarkup:
    "Клавиатура подтверждения бронирования"
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Подтвердить")],
            [KeyboardButton(text="❌ Отменить")],
            [KeyboardButton(text="◀️ Назад")],
        ],
        resize_keyboard=True,
    )


def get_settings_keyboard() -> ReplyKeyboardMarkup:
    "Клавиатура для настроек"
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔔 Уведомления")],
            [KeyboardButton(text="◀️ Назад")],
        ],
        resize_keyboard=True,
    )


def get_backbutton_keyboard() -> ReplyKeyboardMarkup:
    "Клавиатура с кнопкой назад"
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="◀️ Назад")],
        ],
        resize_keyboard=True,
    )
