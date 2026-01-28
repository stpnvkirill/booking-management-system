# ruff: noqa: RUF001
"""Helper functions for booking routes."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.infrastructure.database import BotConfig, Resource

if TYPE_CHECKING:
    pass

# Constants for date/time parsing
MIN_DATE_PARTS = 2
TIME_RANGE_PARTS = 2
DATE_FORMATS = ("%Y-%m-%d", "%d.%m.%Y")
TIME_FORMAT = "%H:%M"
MAX_BOOKINGS_LIST = 10


async def get_customer_id(bot_id: int) -> UUID:
    """Get customer_id from bot_id via BotConfig."""
    bot_cfg = await BotConfig.get(id=bot_id)
    return bot_cfg.owner_id


def main_back_inline() -> InlineKeyboardMarkup:
    """Create inline keyboard with back to main menu button."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ В главное меню",
                    callback_data="nav:main",
                ),
            ],
        ],
    )


def resources_inline(resources: list[Resource]) -> InlineKeyboardMarkup:
    """Create inline keyboard with list of resources."""
    rows: list[list[InlineKeyboardButton]] = []
    for r in resources:
        rows.append(
            [
                InlineKeyboardButton(
                    text=r.name,
                    callback_data=f"booking:resource:{r.id}",
                ),
            ],
        )
    rows.append(
        [InlineKeyboardButton(text="⬅️ В главное меню", callback_data="nav:main")],
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def format_dt(dt: datetime) -> str:
    """Format datetime to string."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%d.%m.%Y %H:%M UTC")


def format_short_dt(dt: datetime) -> str:
    """Format datetime to short string (date and time only)."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%d.%m %H:%M")


def format_bookings_list(bookings: list) -> str:
    """Format list of bookings for display."""
    if not bookings:
        return "Нет забронированных слотов."
    
    lines = ["📅 *Занятые слоты:*\n"]
    for booking in bookings[:MAX_BOOKINGS_LIST]:  # Limit to 10 most recent
        start = format_short_dt(booking.start_time)
        end = format_short_dt(booking.end_time)
        lines.append(f"🔴 {start} - {end}")
    
    if len(bookings) > MAX_BOOKINGS_LIST:
        lines.append(f"\n... и еще {len(bookings) - 10} бронирований")
    
    return "\n".join(lines)


def get_status_emoji(is_available: bool) -> str:
    """Return emoji for resource status: green circle if available, red if busy."""
    return "🟢" if is_available else "🔴"


def parse_period(text: str) -> tuple[datetime, datetime] | None:
    """
    Parse date and time period from text.

    Supported formats (minimal, for bot UX):
    - 2026-01-26 10:00-12:00
    - 26.01.2026 10:00-12:00
    - 2026-01-26 10:00 12:00
    - 26.01.2026 10:00 12:00
    Times are interpreted as UTC if timezone not specified.
    """
    raw = " ".join(text.strip().split())
    if not raw:
        return None

    # Split by space into date + time part(s)
    parts = raw.split(" ")
    if len(parts) < MIN_DATE_PARTS:
        return None
    date_part = parts[0]
    time_part = " ".join(parts[1:])

    # Parse date
    date_obj = None
    for fmt in DATE_FORMATS:
        try:
            date_obj = datetime.strptime(date_part, fmt).date()  # noqa: DTZ007
            break
        except ValueError:
            continue
    if date_obj is None:
        return None

    # Parse times (either "HH:MM-HH:MM" or "HH:MM HH:MM")
    if "-" in time_part:
        t1s, t2s = [s.strip() for s in time_part.split("-", 1)]
    else:
        t_parts = time_part.split(" ")
        if len(t_parts) != TIME_RANGE_PARTS:
            return None
        t1s, t2s = t_parts

    try:
        t1 = datetime.strptime(t1s, TIME_FORMAT).time()  # noqa: DTZ007
        t2 = datetime.strptime(t2s, TIME_FORMAT).time()  # noqa: DTZ007
    except ValueError:
        return None

    start = datetime.combine(date_obj, t1).replace(tzinfo=timezone.utc)
    end = datetime.combine(date_obj, t2).replace(tzinfo=timezone.utc)
    return (start, end)


