from aiogram import Router

from .admin import create_admin_router
from .echo import get_echo_router
from .ping import get_ping_router


def create_router() -> Router:
    router: Router = Router()

    router.include_router(get_ping_router())
    router.include_router(get_echo_router())
    return router
