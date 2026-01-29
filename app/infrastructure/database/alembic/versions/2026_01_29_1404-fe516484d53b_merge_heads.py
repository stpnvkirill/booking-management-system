"""merge heads

Revision ID: fe516484d53b
Revises: a4ed92b554b0, a1b2c3d4e5f6
Create Date: 2026-01-29 14:04:26.967599

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fe516484d53b"
down_revision: Union[str, None] = ("a4ed92b554b0", "a1b2c3d4e5f6")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
