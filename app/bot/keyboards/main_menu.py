from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def get_main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Забронировать")],
            [KeyboardButton(text="🗓 Мои бронирования")],
            [KeyboardButton(text="⭐️ Оставить отзыв")],
            [KeyboardButton(text="⚙️ Настройки")],
        ],
        resize_keyboard=True,
    )


def get_backbutton_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="◀️ Назад")]],
        resize_keyboard=True,
    )
