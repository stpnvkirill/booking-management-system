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


class ResourceUpdate(BaseModel):
    """Schema for partial resource update (PATCH /api/resources/{id})."""

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None)
    resource_type: str | None = Field(None)
    location: str | None = Field(None)
    price_per_hour: int | None = Field(None, ge=0)


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

    class Config:
        from_attributes = True
