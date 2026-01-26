from __future__ import annotations

import asyncio
from contextlib import suppress
from datetime import datetime, timezone
import logging
from typing import TYPE_CHECKING

import sqlalchemy as sa

from app.depends import AsyncSession, provider
from app.infrastructure.database import Booking

if TYPE_CHECKING:
    import uuid as uuid_lib

logger = logging.getLogger(__name__)


class BookingCompletionWatcher:
    """Background watcher that logs completed booking IDs."""

    def __init__(self, poll_interval_seconds: int = 30):
        self.poll_interval_seconds = poll_interval_seconds
        self._watcher_task: asyncio.Task | None = None
        self._logged_booking_ids: set[int] = set()

    @provider.inject_session
    async def _get_bookings_ready_for_logging(
        self,
        *,
        session: AsyncSession | None = None,
    ) -> list[int]:
        """
        Returns booking IDs that are completed and have passed the delay window.
        Filters by current user if available.
        """
        stmt = sa.select(Booking.id).where(
            Booking.end_time <= datetime.now(timezone.utc),
        )

        # Filter by current user if available
        current_user = provider.current_user
        if current_user is not None:
            stmt = stmt.where(Booking.user_id == current_user.id)

        stmt = stmt.order_by(Booking.end_time.asc())
        return list((await session.execute(stmt)).scalars().all())

    @provider.inject_session
    async def _booking_exists(
        self,
        booking_id: int,
        session: AsyncSession | None = None,
    ) -> bool:
        return (await Booking.get(id=booking_id, session=session)) is not None

    @provider.inject_session
    async def _booking_belongs_to_user(
        self,
        booking_id: int,
        user_id: uuid_lib.UUID,
        session: AsyncSession | None = None,
    ) -> bool:
        """Check if booking belongs to the specified user."""
        booking = await Booking.get(id=booking_id, session=session)
        return booking is not None and booking.user_id == user_id

    async def _watch_loop(self) -> None:
        try:
            while True:
                ready_ids = await self._get_bookings_ready_for_logging()

                current_user = provider.current_user
                for booking_id in ready_ids:
                    if booking_id in self._logged_booking_ids:
                        continue
                    if not await self._booking_exists(booking_id):
                        continue

                    # Additional check: verify booking belongs to current user if set
                    if current_user is not None:  # noqa: SIM102
                        if not await self._booking_belongs_to_user(
                            booking_id,
                            current_user.id,
                        ):
                            continue

                    self._logged_booking_ids.add(booking_id)
                    logger.info("Booking completed: id=%s", booking_id)

                await asyncio.sleep(self.poll_interval_seconds)
        except asyncio.CancelledError:
            raise

    async def start(self) -> None:
        """Start background watcher that logs completed booking IDs."""
        if self._watcher_task is not None and not self._watcher_task.done():
            return
        self._watcher_task = asyncio.create_task(self._watch_loop())

    async def stop(self) -> None:
        """Stop the background watcher (called on app shutdown)."""
        if self._watcher_task is None:
            return
        if not self._watcher_task.done():
            self._watcher_task.cancel()
            with suppress(asyncio.CancelledError):
                await self._watcher_task
        self._watcher_task = None


# Module-level instance for backward compatibility
_watcher = BookingCompletionWatcher()


async def start_booking_completion_watcher() -> None:
    """Start background watcher that logs completed booking IDs after 15 minutes."""
    await _watcher.start()


async def stop_booking_completion_watcher() -> None:
    """Stop the background watcher (called on app shutdown)."""
    await _watcher.stop()
