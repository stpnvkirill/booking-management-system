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
    settings: so.Mapped[dict] = so.mapped_column(JSONB, server_default="{}")
