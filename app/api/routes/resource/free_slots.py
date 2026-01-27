"""
GET /api/resources/{resource_id}/free_slots - list free slots for resource
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
import sqlalchemy as sa

from app.api.security import security
from app.depends import AsyncSession, provider
from app.domain.services.resource import resource_service
from app.infrastructure.database import Booking

from .schema import FreeSlotResponse

if TYPE_CHECKING:
    from app.infrastructure.database.models.users import User

router = APIRouter()


class FreeSlotsQueryParams:
    """Query params for free slots; grouped to satisfy linting argument limit."""

    def __init__(
        self,
        start: Annotated[
            datetime,
            Query(..., description="Interval start (ISO datetime with timezone)"),
        ],
        end: Annotated[
            datetime,
            Query(..., description="Interval end (ISO datetime with timezone)"),
        ],
        slot: Annotated[
            int,
            Query(..., gt=0, description="Slot size in seconds"),
        ],
    ):
        self.start = start
        self.end = end
        self.slot = slot


def _merge_intervals(
    intervals: list[tuple[datetime, datetime]],
) -> list[tuple[datetime, datetime]]:
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda x: x[0])
    merged: list[tuple[datetime, datetime]] = [intervals[0]]
    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


@router.get(
    "/{resource_id}/free_slots",
    response_model=list[FreeSlotResponse],
    summary="Get free slots for resource",
)
async def get_free_slots(
    resource_id: int,
    params: Annotated[FreeSlotsQueryParams, Depends()],
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    start = params.start
    end = params.end
    slot = params.slot

    # Validate interval
    if start.tzinfo is None or end.tzinfo is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start and end must be timezone-aware datetimes",
        )
    if end <= start:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="end must be after start",
        )

    # Permission/resource existence check (returns None if not found or access denied)
    resource = await resource_service.get_resource(
        resource_id=resource_id,
        current_user=current_user,
        session=session,
    )
    if resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found or access denied",
        )

    # Load bookings that overlap requested interval
    stmt = sa.select(Booking).where(
        sa.and_(
            Booking.resource_id == resource_id,
            Booking.start_time < end,
            Booking.end_time > start,
        ),
    )
    result = await session.scalars(stmt)
    bookings = list(result.all())

    busy = _merge_intervals(
        [
            (max(b.start_time, start), min(b.end_time, end))
            for b in bookings
            if b.start_time < end and b.end_time > start
        ],
    )

    # Build free intervals (gaps between busy intervals)
    free_intervals: list[tuple[datetime, datetime]] = []
    cursor = start
    for b_start, b_end in busy:
        if cursor < b_start:
            free_intervals.append((cursor, b_start))
        cursor = max(cursor, b_end)
    if cursor < end:
        free_intervals.append((cursor, end))

    # Split free intervals into fixed-size slots
    slot_delta = timedelta(seconds=slot)
    free_slots: list[FreeSlotResponse] = []
    for free_start, free_end in free_intervals:
        t = free_start
        while t + slot_delta <= free_end:
            free_slots.append(FreeSlotResponse(start_time=t, end_time=t + slot_delta))
            t = t + slot_delta

    return free_slots
