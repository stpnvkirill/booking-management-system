from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


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
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏨 Отель")],
            [KeyboardButton(text="🏠 Квартира")],
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