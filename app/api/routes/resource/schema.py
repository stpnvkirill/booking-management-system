"""Pydantic schemas for resource operations."""

from datetime import datetime
import uuid

from pydantic import BaseModel, Field


class ResourceCreate(BaseModel):
    """Schema for creating a resource (POST /api/resources)."""

    customer_id: uuid.UUID | None = Field(
        None,
        description="Customer ID. If not provided, uses user's customer.",
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Resource name",
    )
    description: str | None = Field(None, description="Resource description")
    resource_type: str | None = Field(
        None,
        description="Resource type (квартира/дом/студия/офис)",
    )
    location: str | None = Field(None, description="Resource location (free-form)")
    price_per_hour: int | None = Field(None, ge=0, description="Price per hour")
    available_date: datetime
    available_start: datetime
    available_end: datetime


class ResourceUpdate(BaseModel):
    """Schema for partial resource update (PATCH /api/resources/{id})."""

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None)
    resource_type: str | None = Field(None)
    location: str | None = Field(None)
    price_per_hour: int | None = Field(None, ge=0)
    available_date: datetime
    available_start: datetime
    available_end: datetime


class ResourceResponse(BaseModel):
    """Response schema with resource data."""

    id: int
    customer_id: uuid.UUID
    name: str
    description: str | None = None
    resource_type: str | None = None
    location: str | None = None
    price_per_hour: int | None = None
    created_at: datetime
    available_date: datetime
    available_start: datetime
    available_end: datetime

    class Config:
        from_attributes = True


class FreeSlotResponse(BaseModel):
    """Response schema for a free time slot."""

    start_time: datetime = Field(..., description="Slot start time (ISO format)")
    end_time: datetime = Field(..., description="Slot end time (ISO format)")
