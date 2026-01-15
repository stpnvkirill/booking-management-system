import uuid as uuid_lib

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID
import sqlalchemy.orm as so

from app.infrastructure.database.models.shared import (
    Base,
    BaseWithDt,
    CreatedMixin,
)


class User(BaseWithDt):
    __tablename__ = "users"

    id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        server_default=sa.func.uuidv7(),
        primary_key=True,
    )
    tlg_id: so.Mapped[int | None] = so.mapped_column(sa.BigInteger, unique=True)

    first_name: so.Mapped[str | None] = so.mapped_column()
    last_name: so.Mapped[str | None] = so.mapped_column()
    username: so.Mapped[str | None] = so.mapped_column()

    language_code: so.Mapped[str | None] = so.mapped_column()
    api_token: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        server_default=sa.func.uuidv7(),
    )
    customer_id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        sa.ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
    )

    def __repr__(self):
        return f"User #{self.id}"


class Customer(Base, CreatedMixin):
    __tablename__ = "customers"

    id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        server_default=sa.func.uuidv7(),
        primary_key=True,
    )
    name: so.Mapped[str] = so.mapped_column(
        sa.VARCHAR(50),
    )

    owner_id: so.Mapped[uuid_lib.UUID] = so.mapped_column(UUID, sa.ForeignKey(User.id))


class CustomerAdmin(Base, CreatedMixin):
    __tablename__ = "customer_admins"

    user_id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        sa.ForeignKey(User.id),
        primary_key=True,
    )
    customer_id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        sa.ForeignKey(Customer.id),
        primary_key=True,
    )


class CustomerMember(Base, CreatedMixin):
    __tablename__ = "customer_members"

    user_id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        sa.ForeignKey(User.id),
        primary_key=True,
    )
    customer_id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        sa.ForeignKey(Customer.id),
        primary_key=True,
    )


class BotConfig(BaseWithDt):
    __tablename__ = "bot_configs"

    id: so.Mapped[int] = so.mapped_column(
        sa.BigInteger,
        primary_key=True,
    )
    token: so.Mapped[str] = so.mapped_column(unique=True)
    username: so.Mapped[str] = so.mapped_column(unique=True)
    name: so.Mapped[str] = so.mapped_column(unique=True)
    owner_id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        sa.ForeignKey(Customer.id),
        unique=True,
    )
    customer_id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        sa.ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
    )
    settings: so.Mapped[dict] = so.mapped_column(JSONB, server_default="{}")


class Resource(Base, CreatedMixin):
    __tablename__ = "resources"

    id: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: so.Mapped[str] = so.mapped_column(sa.VARCHAR(255), nullable=False)
    customer_id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        sa.ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
    )


class Booking(BaseWithDt):
    __tablename__ = "bookings"

    id: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )
    resource_id: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        sa.ForeignKey("resources.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    start_time: so.Mapped[sa.DateTime] = so.mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
    )
    end_time: so.Mapped[sa.DateTime] = so.mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
    )
    customer_id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        sa.ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
    )

    __table_args__ = (
        sa.UniqueConstraint(
            "resource_id",
            "start_time",
            "end_time",
            name="unique_booking",
        ),
    )


class Feedback(BaseWithDt):
    __tablename__ = "feedbacks"

    id: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )
    booking_id: so.Mapped[int] = so.mapped_column(
        sa.Integer,
        sa.ForeignKey("bookings.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    comment: so.Mapped[str | None] = so.mapped_column(sa.Text)
    rating: so.Mapped[int] = so.mapped_column(
        sa.SmallInteger,
        nullable=False,
    )
    customer_id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        sa.ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
    )


__table_args__ = (sa.CheckConstraint("rating BETWEEN 1 AND 5", name="rating_check"),)
