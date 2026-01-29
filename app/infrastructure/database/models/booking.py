import uuid as uuid_lib

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy.orm as so

from app.infrastructure.database.models.shared import (
    Base,
    BaseWithDt,
    CreatedMixin,
)


class Resource(Base, CreatedMixin):
    __tablename__ = "resources"

    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
    )
    name: so.Mapped[str] = so.mapped_column(sa.VARCHAR(255))
    customer_id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        sa.ForeignKey("customers.id", ondelete="CASCADE"),
    )
    description: so.Mapped[str | None] = so.mapped_column(
        sa.Text,
        nullable=True,
    )
    resource_type: so.Mapped[str | None] = so.mapped_column(
        sa.Enum("квартира", "дом", "студия", "офис", name="resource_type"),
        nullable=True,
    )
    location: so.Mapped[str | None] = so.mapped_column(
        sa.VARCHAR(255),
        nullable=True,
    )
    price_per_hour: so.Mapped[int | None] = so.mapped_column(
        sa.Integer,
        nullable=True,
    )


class Booking(BaseWithDt):
    __tablename__ = "bookings"

    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
    )
    resource_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("resources.id", ondelete="CASCADE"),
    )
    user_id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
    )
    start_time: so.Mapped[sa.DateTime] = so.mapped_column(
        sa.DateTime(timezone=True),
    )
    end_time: so.Mapped[sa.DateTime] = so.mapped_column(
        sa.DateTime(timezone=True),
    )
