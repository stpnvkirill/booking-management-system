"""
GET /api/resources/{resource_id}/free_slots - list free slots for resource.

Supports two modes:
- By interval: start, end, slot. For the day containing "now", slots start from
  current time; for future days, full day is considered.
- By day: date, slot. Slots for that single day (UTC). If date is today,
  slots start from current time; otherwise for the whole day.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.security import security
from app.depends import AsyncSession, provider
from app.domain.services.resource import resource_service
from app.domain.services.resource.resource import FreeSlotsParams
from app.infrastructure.database.models.users import User  # noqa: TC001

from .schema import FreeSlotResponse

router = APIRouter()


def _day_bounds_utc(d: date) -> tuple[datetime, datetime]:
    """Return (start_of_day_utc, end_of_day_utc) for the given date."""
    start = datetime.combine(d, datetime.min.time(), tzinfo=timezone.utc)
    end = start + timedelta(days=1) - timedelta(microseconds=1)
    return start, end


class FreeSlotsQueryParams:
    """Query params for free slots; grouped to satisfy linting argument limit."""

    def __init__(
        self,
        slot: Annotated[
            int,
            Query(..., gt=0, description="Slot size in seconds"),
        ],
        start: Annotated[
            datetime | None,
            Query(description="Interval start (ISO datetime with timezone)"),
        ] = None,
        end: Annotated[
            datetime | None,
            Query(description="Interval end (ISO datetime with timezone)"),
        ] = None,
        date: Annotated[
            date | None,
            Query(
                description="Slots for this single day (UTC). Use date or start+end.",
            ),
        ] = None,
    ):
        self.slot = slot
        self.start = start
        self.end = end
        self.date = date


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
    if params.date is not None:
        if params.start is not None or params.end is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Use either date or start+end, not both",
            )
        start, end = _day_bounds_utc(params.date)
    else:
        if params.start is None or params.end is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Provide start and end, or date",
            )
        start = params.start
        end = params.end

    try:
        slots = await resource_service.get_free_slots(
            resource_id=resource_id,
            current_user=current_user,
            params=FreeSlotsParams(start=start, end=end, slot=params.slot),
            session=session,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e

    if slots is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found or access denied",
        )

    return [FreeSlotResponse(start_time=s, end_time=e) for (s, e) in slots]
