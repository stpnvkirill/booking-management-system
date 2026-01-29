"""Resource service for handling resource business logic with multitenancy support."""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import UUID

import sqlalchemy as sa

from app.depends import AsyncSession, provider
from app.infrastructure.database import Booking
from app.infrastructure.database.models.booking import Resource
from app.infrastructure.database.models.users import (
    Customer,
    CustomerAdmin,
    CustomerMember,
    User,
)


@dataclass(frozen=True)
class FreeSlotsParams:
    """Params for get_free_slots. slot is size in seconds."""

    start: datetime
    end: datetime
    slot: int


def _merge_intervals(
    intervals: list[tuple[datetime, datetime]],
) -> list[tuple[datetime, datetime]]:
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda x: x[0])
    merged: list[tuple[datetime, datetime]] = [intervals[0]]
    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


@dataclass(frozen=True)
class ResourceCreateParams:
    name: str
    customer_id: UUID | None = None
    description: str | None = None
    resource_type: str | None = None
    location: str | None = None
    price_per_hour: int | None = None


@dataclass(frozen=True)
class ResourceUpdateParams:
    name: str | None = None
    description: str | None = None
    resource_type: str | None = None
    location: str | None = None
    price_per_hour: int | None = None


class ResourceService:
    """Service for resource CRUD operations with multitenancy checks."""

    @provider.inject_session
    async def is_admin_or_owner(
        self,
        user_id: UUID,
        customer_id: UUID,
        session: AsyncSession | None = None,
    ) -> bool:
        """Check if user is admin or owner of the customer."""
        # Check if owner
        customer = await Customer.get_by(
            id=customer_id,
            owner_id=user_id,
            session=session,
        )
        if customer:
            return True

        # Check if admin
        admin = await CustomerAdmin.get_by(
            user_id=user_id,
            customer_id=customer_id,
            session=session,
        )
        return admin is not None

    @provider.inject_session
    async def is_member_or_admin_or_owner(
        self,
        user_id: UUID,
        customer_id: UUID,
        session: AsyncSession | None = None,
    ) -> bool:
        """Check if user is member, admin, or owner of the customer."""
        if await self.is_admin_or_owner(
            user_id=user_id,
            customer_id=customer_id,
            session=session,
        ):
            return True
        member = await CustomerMember.get_by(
            user_id=user_id,
            customer_id=customer_id,
            session=session,
        )
        return member is not None

    @provider.inject_session
    async def get_customer_for_user(
        self,
        user_id: UUID,
        session: AsyncSession | None = None,
    ) -> Customer | None:
        """Get customer where user is owner, admin, or member."""
        # First check if user is owner
        customer = await Customer.get_by(owner_id=user_id, session=session)
        if customer:
            return customer

        # Check if user is admin of any customer
        admin_record = await CustomerAdmin.get_by(user_id=user_id, session=session)
        if admin_record:
            return await Customer.get(id=admin_record.customer_id, session=session)

        member_record = await CustomerMember.get_by(user_id=user_id, session=session)
        if member_record:
            return await Customer.get(id=member_record.customer_id, session=session)

        return None

    @provider.inject_session
    async def create_resource(
        self,
        current_user: User,
        params: ResourceCreateParams,
        session: AsyncSession | None = None,
    ) -> Resource | None:
        """Create a new resource for a customer.

        If customer_id is not provided, uses the customer where user is owner/admin.
        """
        # Determine customer_id
        customer_id = params.customer_id
        if customer_id is None:
            customer = await self.get_customer_for_user(
                user_id=current_user.id,
                session=session,
            )
            if not customer:
                return None
            customer_id = customer.id
        # Verify user has permission for this customer
        elif not await self.is_admin_or_owner(
            user_id=current_user.id,
            customer_id=customer_id,
            session=session,
        ):
            return None

        resource = Resource(
            customer_id=customer_id,
            name=params.name,
            description=params.description,
            resource_type=params.resource_type,
            location=params.location,
            price_per_hour=params.price_per_hour,
        )
        session.add(resource)
        await session.flush()
        await session.refresh(resource)
        return resource

    @provider.inject_session
    async def get_resources_for_customer(
        self,
        current_user: User,
        customer_id: UUID | None = None,
        skip: int = 0,
        limit: int = 100,
        session: AsyncSession | None = None,
    ) -> list[Resource]:
        """Get resources filtered by customer (multitenancy).

        Returns resources for customers where user is member, admin, or owner.
        """
        if customer_id is None:
            customer = await self.get_customer_for_user(
                user_id=current_user.id,
                session=session,
            )
            if not customer:
                return []
            customer_id = customer.id
        elif not await self.is_member_or_admin_or_owner(
            user_id=current_user.id,
            customer_id=customer_id,
            session=session,
        ):
            return []

        stmt = (
            sa.select(Resource)
            .where(Resource.customer_id == customer_id)
            .offset(skip)
            .limit(limit)
        )
        result = await session.scalars(stmt)
        return list(result.all())

    @provider.inject_session
    async def get_resource(
        self,
        resource_id: int,
        current_user: User,
        session: AsyncSession | None = None,
    ) -> Resource | None:
        """Get a single resource with permission check."""
        stmt = sa.select(Resource).where(Resource.id == resource_id)
        resource = await session.scalar(stmt)

        if not resource:
            return None

        # Check permission
        if not await self.is_admin_or_owner(
            user_id=current_user.id,
            customer_id=resource.customer_id,
            session=session,
        ):
            return None

        return resource

    @provider.inject_session
    async def update_resource(
        self,
        resource_id: int,
        current_user: User,
        params: ResourceUpdateParams,
        session: AsyncSession | None = None,
    ) -> Resource | None:
        """Update resource with permission check."""
        resource = await self.get_resource(
            resource_id=resource_id,
            current_user=current_user,
            session=session,
        )
        if not resource:
            return None

        if params.name is not None:
            resource.name = params.name
        if params.description is not None:
            resource.description = params.description
        if params.resource_type is not None:
            resource.resource_type = params.resource_type
        if params.location is not None:
            resource.location = params.location
        if params.price_per_hour is not None:
            resource.price_per_hour = params.price_per_hour

        await session.flush()
        await session.refresh(resource)
        return resource

    @provider.inject_session
    async def get_all_resources(
        self,
        skip: int = 0,
        limit: int = 100,
        session: AsyncSession | None = None,
    ) -> list[Resource]:
        """Get all resources (no multitenancy filter)."""
        stmt = sa.select(Resource).offset(skip).limit(limit)
        result = await session.scalars(stmt)
        return list(result.all())

    @provider.inject_session
    async def delete_resource(
        self,
        resource_id: int,
        current_user: User,
        session: AsyncSession | None = None,
    ) -> bool:
        """Delete resource with permission check.

        Note: Currently performs hard delete as model lacks is_active field.
        """
        resource = await self.get_resource(
            resource_id=resource_id,
            current_user=current_user,
            session=session,
        )
        if not resource:
            return False

        await session.delete(resource)
        return True

    @provider.inject_session
    async def get_free_slots(
        self,
        resource_id: int,
        current_user: User,
        params: FreeSlotsParams,
        session: AsyncSession | None = None,
    ) -> list[tuple[datetime, datetime]] | None:
        """Return list of free slots (start,end) for given interval and slot size.

        Returns None if resource not found or access denied (multitenancy).
        Raises ValueError for invalid params.
        """
        start = params.start
        end = params.end
        slot = params.slot

        if start.tzinfo is None or end.tzinfo is None:
            msg = "start and end must be timezone-aware datetimes"
            raise ValueError(msg)
        if end <= start:
            msg = "end must be after start"
            raise ValueError(msg)
        if (end - start) > timedelta(days=1):
            msg = "interval duration must not exceed 1 days"
            raise ValueError(msg)
        if slot <= 0:
            msg = "slot must be a positive integer (seconds)"
            raise ValueError(msg)

        now = datetime.now(timezone.utc)
        effective_start = max(start, now)
        if effective_start >= end:
            return []

        # Permission/resource existence check
        resource = await self.get_resource(
            resource_id=resource_id,
            current_user=current_user,
            session=session,
        )
        if resource is None:
            return None

        # Load bookings that overlap requested interval (SQL does the filtering)
        stmt = sa.select(Booking).where(
            sa.and_(
                Booking.resource_id == resource_id,
                Booking.start_time < end,
                Booking.end_time > start,
            ),
        )
        result = await session.scalars(stmt)
        bookings = list(result.all())

        busy = _merge_intervals(
            [
                (max(b.start_time, effective_start), min(b.end_time, end))
                for b in bookings
            ],
        )

        # Build free intervals (gaps between busy intervals)
        free_intervals: list[tuple[datetime, datetime]] = []
        cursor = effective_start
        for b_start, b_end in busy:
            if cursor < b_start:
                free_intervals.append((cursor, b_start))
            cursor = max(cursor, b_end)
        if cursor < end:
            free_intervals.append((cursor, end))

        # Split free intervals into fixed-size slots
        slot_delta = timedelta(seconds=slot)
        free_slots: list[tuple[datetime, datetime]] = []
        for free_start, free_end in free_intervals:
            t = free_start
            while t + slot_delta <= free_end:
                free_slots.append((t, t + slot_delta))
                t = t + slot_delta

        return free_slots


resource_service = ResourceService()
