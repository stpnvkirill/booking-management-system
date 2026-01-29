"""Main menu routes - объединение мелких роутеров."""

from aiogram import Router
from aiogram.filters import command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.bot.filters.chat_type import OnlyPrivateChatFilter
from app.bot.handler import handler
from app.bot.keyboards.main_menu import get_main_menu, get_settings_keyboard


def get_main_menu_router() -> Router:
    """Create router for main menu handlers."""
    router = Router()

    @router.message(OnlyPrivateChatFilter(), command.Command("start"))
    @handler
    async def start_handler(message: Message):
        """Handle /start command."""
        await message.answer(
            "👋 Привет!\n"
            "Я помогу тебе забронировать ресурс, "  # noqa: RUF001
            "посмотреть твои бронирования и управлять настройками.",
            reply_markup=get_main_menu(),
        )

    @router.message(lambda m: m.text == "◀️ Назад")
    @handler
    async def back_button(message: Message, state: FSMContext):
        """Handle back button."""
        await state.clear()
        await message.answer(
            "Вы вернулись в главное меню",
            reply_markup=get_main_menu(),
        )

    @router.message(lambda m: m.text == "⚙️ Настройки")
    @handler
    async def start_settings(message: Message):
        """Handle settings button."""
        await message.answer(
            "Выберите настройки: ",
            reply_markup=get_settings_keyboard(),
        )

    @router.message(lambda m: m.text == "⭐️ Оставить отзыв")
    @handler
    async def start_reviews(message: Message, state: FSMContext):
        """Handle reviews button."""
        await state.clear()
        await message.answer(
            "Функция отзывов временно недоступна. ",
            reply_markup=get_main_menu(),
        )

    return router
