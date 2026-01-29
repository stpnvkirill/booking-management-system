from aiogram import Router

from .handlers import get_admin_handlers_router


def create_admin_router() -> Router:
    router: Router = Router()
    router.include_router(get_admin_handlers_router())
    return router
