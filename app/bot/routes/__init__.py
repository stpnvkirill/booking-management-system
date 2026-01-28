"""Booking routes module."""

from aiogram import Router

from .create import get_create_router
from .list import get_list_router
from .navigation import get_navigation_router


def get_bookings_router() -> Router:
    """Create main bookings router combining all sub-routers."""
    router = Router()
    router.include_router(get_create_router())
    router.include_router(get_list_router())
    router.include_router(get_navigation_router())
    return router

