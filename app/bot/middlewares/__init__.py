from .logging import LoggingMiddleware
from .user import UserMiddleware


def register_middleware(dp):
    dp.update.outer_middleware(UserMiddleware())
    dp.update.outer_middleware(LoggingMiddleware())
