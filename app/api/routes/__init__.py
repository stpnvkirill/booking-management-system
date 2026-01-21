from .customer import router as customer_router
from .telegram import router as telegram_router
from .user import router as user_router

routes = [
    user_router,
    customer_router,
    telegram_router,
]

__all__ = [
    "routes",
]
