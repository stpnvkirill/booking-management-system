from aiogram import Router

from app.bot.routes.bookings import get_bookings_router
from app.bot.routes.button_handler import get_button_handler_router
from app.bot.routes.reviews import get_reviews_router
from app.bot.routes.settings import get_settings_router

from .admin import create_admin_router
from .echo import get_echo_router
from .ping import get_ping_router
from .start import get_start_router


def create_router() -> Router:
    router: Router = Router()
    router.include_router(get_button_handler_router())
    router.include_router(get_bookings_router())
    router.include_router(get_settings_router())
    router.include_router(get_reviews_router())
    router.include_router(get_start_router())
    router.include_router(get_ping_router())
    router.include_router(get_echo_router())
    return router
