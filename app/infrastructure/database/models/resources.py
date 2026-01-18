import enum
import uuid as uuid_lib

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID
import sqlalchemy.orm as so

from app.infrastructure.database.models.shared import BaseWithDt
from app.infrastructure.database.models.users import Customer


class ResourceType(str, enum.Enum):
    MEETING_ROOM = "meeting_room"
    SPECIALIST = "specialist"
    EQUIPMENT = "equipment"


class Resource(BaseWithDt):
    __tablename__ = "resources"

    id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        server_default=sa.func.uuidv7(),
        primary_key=True,
    )
    
    customer_id: so.Mapped[uuid_lib.UUID] = so.mapped_column(
        UUID,
        sa.ForeignKey(Customer.id),
        nullable=False
    )

    type: so.Mapped[ResourceType] = so.mapped_column(
        sa.Enum(ResourceType),
        nullable=False
    )

    name: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    description: so.Mapped[str | None] = so.mapped_column(sa.Text, nullable=True)
    
    # Specific fields
    capacity: so.Mapped[int | None] = so.mapped_column(sa.Integer, nullable=True)
    position: so.Mapped[str | None] = so.mapped_column(sa.String, nullable=True)
    schedule: so.Mapped[dict | None] = so.mapped_column(JSONB, nullable=True)

    is_active: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"Resource(id={self.id}, name={self.name}, type={self.type})"
