from aiogram import Router

from app.bot.middlewares.database import DatabaseMiddleware
from app.bot.routes.admin.middlewares import (
    RoleCheckMiddleware,
)

from .handlers import (
    get_admin_handlers_router,
    get_create_owner_router,
)


def create_admin_router() -> Router:
    router = Router()
    router.include_router(get_create_owner_router())
    admin_panel_router = Router()
    admin_panel_router.message.middleware(DatabaseMiddleware())
    admin_panel_router.callback_query.middleware(DatabaseMiddleware())
    admin_panel_router.message.middleware(RoleCheckMiddleware())
    admin_panel_router.callback_query.middleware(RoleCheckMiddleware())

    handlers_router = get_admin_handlers_router()
    admin_panel_router.include_router(handlers_router)

    router.include_router(admin_panel_router)

    return router
