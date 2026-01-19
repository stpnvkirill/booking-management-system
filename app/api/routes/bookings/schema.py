from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class BookingCreate(BaseModel):
    """Schema for creating a new booking."""

    resource_id: int = Field(..., description="ID of the resource to book")
    start_time: datetime = Field(..., description="Booking start time (ISO format)")
    end_time: datetime = Field(..., description="Booking end time (ISO format)")


class BookingResponse(BaseModel):
    """Schema for booking response."""

    id: int
    user_id: UUID
    resource_id: int
    resource_name: str | None = None
    start_time: datetime
    end_time: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


class BookingListResponse(BaseModel):
    """Schema for booking list response."""

    bookings: list[BookingResponse]
