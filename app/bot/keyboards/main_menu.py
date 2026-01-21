from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
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


def get_resource_type_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏢 Переговорная")],
            [KeyboardButton(text="💻 Рабочее место")],
            [KeyboardButton(text="◀️ Назад")],
        ],
        resize_keyboard=True,
    )
    buttons = [
        [InlineKeyboardButton(text="🏢 Переговорная", callback_data="type:meeting")],
        [InlineKeyboardButton(text="💻 Рабочее место", callback_data="type:workspace")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_resources_keyboard(
    resources: list[str],
    busy: set[str] | None = None,
) -> ReplyKeyboardMarkup:
    busy = busy or set()
    rows = []
    for resource in resources:
        status = "🔴" if resource in busy else "🟢"
        rows.append([KeyboardButton(text=f"{status} {resource}")])
    rows.append([KeyboardButton(text="◀️ Назад")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def get_date_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Сегодня"), KeyboardButton(text="📅 Завтра")],
            [KeyboardButton(text="Ввести дату")],
            [KeyboardButton(text="◀️ Назад")],
        ],
        resize_keyboard=True,
    )


def get_time_keyboard(slots: list[str]) -> ReplyKeyboardMarkup:
    rows: list[list[KeyboardButton]] = []
    for slot in slots:
        rows.append([KeyboardButton(text=slot)])
    rows.append([KeyboardButton(text="◀️ Назад")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def get_confirm_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Подтвердить")],
            [KeyboardButton(text="❌ Отменить")],
            [KeyboardButton(text="◀️ Назад")],
        ],
        resize_keyboard=True,
    )


def get_backbutton_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="◀️ Назад")]],
        resize_keyboard=True,
    )
    
def get_resource_type_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏢 Переговорная", callback_data="type:meeting")],
        [InlineKeyboardButton(text="💻 Рабочее место", callback_data="type:workspace")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back:main")],
    ])

def get_resource_type_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏢 Переговорная",
                    callback_data="type:meeting",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="💻 Рабочее место",
                    callback_data="type:workspace",
                ),
            ],
        ],
    )

def get_resources_inline(
    resources: list[str],
    busy: set[str] | None = None,
) -> InlineKeyboardMarkup:
    busy = busy or set()
    rows = []

    for idx, resource in enumerate(resources, start=1):
        status = "🔴" if resource in busy else "🟢"
        rows.append([
            InlineKeyboardButton(
                text=f"{status} {resource}",
                callback_data=f"resource:{idx}",
            )
        ])
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"{status} {resource}",
                    callback_data=f"resource:{idx}",
                ),
            ],
        )

    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back:type")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def get_date_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Сегодня", callback_data="date:today")],
        [InlineKeyboardButton(text="📅 Завтра", callback_data="date:tomorrow")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back:resource")],
    ])

def get_date_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📅 Сегодня", callback_data="date:today")],
            [InlineKeyboardButton(text="📅 Завтра", callback_data="date:tomorrow")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back:resource")],
        ],
    )

def get_time_inline(slots: list[str]) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                text=slot,
                callback_data=f"time:{slot}",
            )
            ),
        ]
        for slot in slots
    ]

    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back:date")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def get_confirm_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm:yes")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="confirm:no")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back:time")],
    ])

def get_success_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ В главное меню", callback_data="back:main")],
    ])

def get_confirm_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm:yes")],
            [InlineKeyboardButton(text="❌ Отменить", callback_data="confirm:no")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back:time")],
        ],
    )


def get_success_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ В главное меню", callback_data="back:main")],
        ],
    )

def get_my_bookings_inline(bookings: list[str]) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                text=booking,
                callback_data=f"booking:{idx}",
            )
            ),
        ]
        for idx, booking in enumerate(bookings, start=1)
    ]

    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back:main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_booking_details_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отменить", callback_data="booking:cancel")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="booking:list")],
    ])
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отменить", callback_data="booking:cancel")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="booking:list")],
        ],
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
)
