"""Navigation handlers."""

import contextlib

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from app.bot.handler import handler
from app.bot.keyboards.main_menu import get_main_menu


def get_navigation_router() -> Router:
    """Create router for navigation handlers."""
    router = Router()

    @router.callback_query(lambda c: c.data == "nav:main")
    @handler
    async def nav_main(callback: types.CallbackQuery, state: FSMContext):
        """Navigate to main menu."""
        await state.clear()
        await callback.message.answer("Главное меню:", reply_markup=get_main_menu())
        with contextlib.suppress(Exception):
            await callback.message.delete()
        await callback.answer()

    return router
