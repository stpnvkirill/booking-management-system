from .database import DatabaseMiddleware
from .logging import LoggingMiddleware
from .metrics import MetricsMiddleware
from .user import UserMiddleware


def register_middleware(dp):
    # DatabaseMiddleware должен быть первым, чтобы предоставить сессию остальным
    dp.update.outer_middleware(DatabaseMiddleware())
    dp.update.outer_middleware(UserMiddleware())
    dp.update.outer_middleware(MetricsMiddleware())
    dp.update.outer_middleware(LoggingMiddleware())
