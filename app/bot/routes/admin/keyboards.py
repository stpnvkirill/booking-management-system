from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏢 Управление заказчиками",
                    callback_data="customers_menu",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="👥 Управление администраторами",
                    callback_data="admins_menu",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="💼 Моя компания",
                    callback_data="my_company",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❓ Помощь",
                    callback_data="help",
                ),
            ],
        ],
    )
