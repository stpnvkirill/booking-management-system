"""add_booking_fields_description_type_location

Revision ID: a1b2c3d4e5f6
Revises: 887a31edf9cf
Create Date: 2026-01-26 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "887a31edf9cf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum type for booking_type
    booking_type_enum = sa.Enum(
        "квартира", "дом", "студия", "офис", name="booking_type"
    )
    booking_type_enum.create(op.get_bind(), checkfirst=True)

    # Add new columns to bookings table (with existence check)
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col["name"] for col in inspector.get_columns("bookings")]

    if "description" not in columns:
        op.add_column(
            "bookings",
            sa.Column("description", sa.Text(), nullable=True),
        )
    if "booking_type" not in columns:
        op.add_column(
            "bookings",
            sa.Column("booking_type", booking_type_enum, nullable=True),
        )
    if "location" not in columns:
        op.add_column(
            "bookings",
            sa.Column("location", sa.VARCHAR(length=255), nullable=True),
        )


def downgrade() -> None:
    # Remove columns
    op.drop_column("bookings", "location")
    op.drop_column("bookings", "booking_type")
    op.drop_column("bookings", "description")

    # Drop enum type
    sa.Enum(name="booking_type").drop(op.get_bind(), checkfirst=True)
