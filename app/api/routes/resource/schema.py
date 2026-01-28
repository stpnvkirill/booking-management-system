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


class ResourceUpdate(BaseModel):
    """Schema for partial resource update (PATCH /api/resources/{id})."""

    name: str | None = Field(None, min_length=1, max_length=255)


class ResourceResponse(BaseModel):
    """Response schema with resource data."""

    id: int
    customer_id: uuid.UUID
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


class FreeSlotResponse(BaseModel):
    """Response schema for a free time slot."""

    start_time: datetime = Field(..., description="Slot start time (ISO format)")
    end_time: datetime = Field(..., description="Slot end time (ISO format)")
