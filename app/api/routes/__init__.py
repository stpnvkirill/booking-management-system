from .bookings import router as bookings_router
from .customer import router as customer_router
from .ping import router as ping_router
from .telegram import router as telegram_router
from .user import router as user_router

routes = [
    user_router,
    customer_router,
    bookings_router,
    telegram_router,
    ping_router,
]

__all__ = [
    "routes",
]
