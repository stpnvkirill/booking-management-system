"""ensure_resource_fields

Revision ID: 9b2d6c1f8a77
Revises: fe516484d53b
Create Date: 2026-01-29 15:00:00.000000

Idempotent migration to ensure Resource columns exist.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9b2d6c1f8a77"
down_revision: Union[str, None] = "fe516484d53b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


RESOURCE_TYPE_ENUM = sa.Enum("квартира", "дом", "студия", "офис", name="resource_type")


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    # Ensure enum exists (and rename old one if present)
    enum_names = {e["name"] for e in inspector.get_enums()}
    if "booking_type" in enum_names and "resource_type" not in enum_names:
        op.execute("ALTER TYPE booking_type RENAME TO resource_type")
    RESOURCE_TYPE_ENUM.create(op.get_bind(), checkfirst=True)

    resource_columns = {col["name"] for col in inspector.get_columns("resources")}
    if "description" not in resource_columns:
        op.add_column("resources", sa.Column("description", sa.Text(), nullable=True))
    if "resource_type" not in resource_columns:
        op.add_column(
            "resources", sa.Column("resource_type", RESOURCE_TYPE_ENUM, nullable=True)
        )
    if "location" not in resource_columns:
        op.add_column(
            "resources", sa.Column("location", sa.VARCHAR(length=255), nullable=True)
        )
    if "price_per_hour" not in resource_columns:
        op.add_column(
            "resources", sa.Column("price_per_hour", sa.Integer(), nullable=True)
        )

    # If old booking columns still exist, drop them (optional hardening)
    booking_columns = {col["name"] for col in inspector.get_columns("bookings")}
    if "location" in booking_columns:
        op.drop_column("bookings", "location")
    if "booking_type" in booking_columns:
        op.drop_column("bookings", "booking_type")
    if "description" in booking_columns:
        op.drop_column("bookings", "description")


def downgrade() -> None:
    # Keep downgrade minimal/safe (no destructive enum drop)
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    resource_columns = {col["name"] for col in inspector.get_columns("resources")}
    if "price_per_hour" in resource_columns:
        op.drop_column("resources", "price_per_hour")
    if "location" in resource_columns:
        op.drop_column("resources", "location")
    if "resource_type" in resource_columns:
        op.drop_column("resources", "resource_type")
    if "description" in resource_columns:
        op.drop_column("resources", "description")
