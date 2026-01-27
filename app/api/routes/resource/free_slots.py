"""
GET /api/resources/{resource_id}/free_slots - list free slots for resource
"""

from __future__ import annotations

from datetime import datetime  # noqa: TC003
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.security import security
from app.depends import AsyncSession, provider
from app.domain.services.resource import resource_service
from app.domain.services.resource.resource import FreeSlotsParams

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
    try:
        slots = await resource_service.get_free_slots(
            resource_id=resource_id,
            current_user=current_user,
            params=FreeSlotsParams(
                start=params.start,
                end=params.end,
                slot_seconds=params.slot,
            ),
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
