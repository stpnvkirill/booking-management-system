from .customer import router as customer_router
from .ping import router as ping_router
from .room import router as room_router
from .telegram import router as telegram_router
from .user import router as user_router

routes = [
    user_router,
    customer_router,
    telegram_router,
    ping_router,
    room_router,
]

__all__ = [
    "routes",
]
