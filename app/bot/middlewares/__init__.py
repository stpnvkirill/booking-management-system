from .database import DatabaseMiddleware
from .logging import LoggingMiddleware
from .user import UserMiddleware


def register_middleware(dp):
    # DatabaseMiddleware должен быть первым, чтобы предоставить сессию остальным
    dp.update.outer_middleware(DatabaseMiddleware())
    dp.update.outer_middleware(UserMiddleware())
    dp.update.outer_middleware(LoggingMiddleware())
