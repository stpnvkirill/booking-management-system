from .logging import LoggingMiddleware
from .metrics import MetricsMiddleware
from .user import UserMiddleware


def register_middleware(dp):
    dp.update.outer_middleware(UserMiddleware())
    dp.update.outer_middleware(MetricsMiddleware())
    dp.update.outer_middleware(LoggingMiddleware())
