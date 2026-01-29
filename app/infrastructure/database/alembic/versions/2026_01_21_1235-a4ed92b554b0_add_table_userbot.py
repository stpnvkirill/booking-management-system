"""add_table_userbot

Revision ID: a4ed92b554b0
Revises: 887a31edf9cf
Create Date: 2026-01-21 12:35:42.903428

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a4ed92b554b0"
down_revision: Union[str, None] = "887a31edf9cf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Make migration idempotent for existing DBs
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if "bot_users" in inspector.get_table_names():
        return

    op.create_table(
        "bot_users",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("bot_id", sa.BigInteger(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk__bot_users__user_id__users"),
        ),
        sa.PrimaryKeyConstraint("user_id", "bot_id", name=op.f("pk__bot_users")),
    )


def downgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if "bot_users" not in inspector.get_table_names():
        return
    op.drop_table("bot_users")
