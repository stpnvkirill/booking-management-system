import uuid as uuid_lib

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy.orm as so

from app.infrastructure.database.models.shared import (
    Base,
    CreatedMixin,
)


class Feedback(Base, CreatedMixin):
    __tablename__ = "feedbacks"

    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
    )
    booking_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("bookings.id", ondelete="CASCADE"),
    )
    user_id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
    )
    comment: so.Mapped[str | None] = so.mapped_column(sa.Text)
    rating: so.Mapped[int] = so.mapped_column(
        sa.SmallInteger,
    )
    customer_id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        sa.ForeignKey("customers.id", ondelete="CASCADE"),
    )

    __table_args__ = (
        sa.CheckConstraint("rating BETWEEN 1 AND 5", name="rating_check"),
    )
