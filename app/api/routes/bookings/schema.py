from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.infrastructure.database.models import BookingType


class BookingCreate(BaseModel):
    """Schema for creating a new booking."""

    customer_id: UUID = Field(
        ...,
        description="ID of the customer who owns the resource",
    )
    resource_id: int = Field(..., description="ID of the resource to book")
    start_time: datetime = Field(..., description="Booking start time (ISO format)")
    end_time: datetime = Field(..., description="Booking end time (ISO format)")
    description: str | None = Field(
        None,
        description="Описание брони",
    )
    booking_type: BookingType | None = Field(
        None,
        description="Тип брони (квартира | дом | студия | офис)",
    )
    location: str | None = Field(
        None,
        description="Расположение (район, вводится пользователем)",
    )


class BookingResponse(BaseModel):
    """Schema for booking response."""

    id: int
    user_id: UUID
    resource_id: int
    resource_name: str | None = None
    start_time: datetime
    end_time: datetime
    description: str | None = None
    booking_type: BookingType | None = None
    location: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class BookingListResponse(BaseModel):
    """Schema for booking list response."""

    bookings: list[BookingResponse]
