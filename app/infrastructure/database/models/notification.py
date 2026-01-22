from datetime import datetime
from typing import TYPE_CHECKING
import uuid as uuid_lib
from zoneinfo import ZoneInfo

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy.orm as so

from app.infrastructure.database.models.shared import BaseWithDt

if TYPE_CHECKING:
    from app.infrastructure.database.models.booking import Booking
    from app.infrastructure.database.models.users import User


class NotificationStatus:
    """Notification statuses."""

    PENDING = "pending"  # Waiting for sending
    PROCESSING = "processing"  # In sending process
    SENT = "sent"  # Successfully sent
    FAILED = "failed"  # Send error


class NotificationType:
    """Notification types."""

    BOOKING_24H = "booking_24h"  # 24 hours before
    BOOKING_1H = "booking_1h"  # 1 hour before
    BOOKING_START = "booking_start"  # Booking start
    BOOKING_END = "booking_end"  # Booking end
    BOOKING_CANCEL = "booking_cancel"  # Booking cancel


class Notification(BaseWithDt):
    """Notification model."""

    __tablename__ = "notifications"

    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
        index=True,
        autoincrement=True,
    )
    type: so.Mapped[str] = so.mapped_column(
        sa.String(20),
        nullable=False,
        index=True,
        comment="Тип уведомления",
    )
    status: so.Mapped[str] = so.mapped_column(
        sa.String(20),
        default=NotificationStatus.PENDING,
        nullable=False,
        index=True,
        comment="Статус уведомления",
    )

    # Relationships
    booking_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("bookings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="ID бронирования",
    )
    user_id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID(as_uuid=True),
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="ID пользователя",
    )

    # Timestamps
    scheduled_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="Время запланированной отправки",
    )
    processed_at: so.Mapped[datetime | None] = so.mapped_column(
        sa.DateTime(timezone=True),
        nullable=True,
        comment="Время фактической отправки",
    )

    # Message info
    message: so.Mapped[str | None] = so.mapped_column(
        sa.Text,
        nullable=True,
        comment="Текст отправленного сообщения",
    )
    error: so.Mapped[str | None] = so.mapped_column(
        sa.Text,
        nullable=True,
        comment="Ошибка при отправке",
    )

    # Relationships
    booking: so.Mapped["Booking"] = so.relationship(
        "Booking",
        back_populates="notifications",
        lazy="select",
    )

    user: so.Mapped["User"] = so.relationship(
        "User",
        backref="notifications",
        lazy="select",
    )

    @property
    def is_due(self) -> bool:
        """Check if it's time to send notification."""
        return datetime.now(ZoneInfo("UTC")) >= self.scheduled_at

    @property
    def can_be_sent(self) -> bool:
        """Check if notification can be sent."""
        return self.status == NotificationStatus.PENDING and self.is_due
