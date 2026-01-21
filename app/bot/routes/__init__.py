from aiogram import Router

from app.api.routes import routes
from app.bot.routes.start import get_start_router

from .echo import get_echo_router


def create_router():
    router = Router()
    router.include_router(get_start_router())
    router.include_router(get_echo_router())
    return router
