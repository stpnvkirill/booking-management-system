"""Booking routes module."""

from aiogram import Router

from .admin import create_admin_router
from .create import get_create_router
from .echo import get_echo_router
from .list import get_list_router
from .main_menu import get_main_menu_router
from .navigation import get_navigation_router
from .ping import get_ping_router


def get_bookings_router() -> Router:
    """Create main bookings router combining all sub-routers."""
    router = Router()
    router.include_router(get_create_router())
    router.include_router(get_list_router())
    router.include_router(get_navigation_router())
    return router


def create_router() -> Router:
    """Create main router for client bot."""
    router = Router()
    router.include_router(get_main_menu_router())
    router.include_router(get_bookings_router())
    router.include_router(get_ping_router())
    router.include_router(get_echo_router())
    return router
