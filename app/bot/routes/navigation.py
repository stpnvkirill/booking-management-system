"""Navigation handlers."""

from typing import TYPE_CHECKING

from aiogram import Router, types

from app.bot.handler import handler
from app.bot.keyboards.main_menu import get_main_menu

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext


def get_navigation_router() -> Router:
    """Create router for navigation handlers."""
    router = Router()

    @router.callback_query(lambda c: c.data == "nav:main")
    @handler
    async def nav_main(callback: types.CallbackQuery, state: FSMContext):
        """Navigate to main menu."""
        await state.clear()
        await callback.message.answer("Главное меню:", reply_markup=get_main_menu())
        try:
            await callback.message.delete()
        except Exception:  # noqa: BLE001
            # Message might already be deleted or inaccessible, ignore
            pass
        await callback.answer()

    return router

