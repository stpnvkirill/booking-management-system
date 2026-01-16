from aiogram import Router

from app.api.routes import routes
from app.bot.routes.booking import get_booking_router
from app.bot.routes.button_handler import get_button_handler_router
from app.bot.routes.my_booking import get_mybooking_router
from app.bot.routes.reviews import get_reviews_router
from app.bot.routes.settings import get_settings_router
from app.bot.routes.start import get_start_router

from .echo import get_echo_router


def create_router():
    router = Router()
    router.include_router(get_mybooking_router())
    router.include_router(get_button_handler_router())
    router.include_router(get_settings_router())
    router.include_router(get_reviews_router())
    router.include_router(get_booking_router())
    router.include_router(get_start_router())
    router.include_router(get_echo_router())
    return router
