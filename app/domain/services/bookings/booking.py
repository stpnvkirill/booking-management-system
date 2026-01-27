from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import UUID

import sqlalchemy as sa

from app.depends import AsyncSession, provider
from app.infrastructure.database import Booking, Resource

# Maximum booking duration: 3 years in the future
MAX_BOOKING_DURATION_DAYS = 365 * 3


@dataclass
class BookingParams:
    """Parameters for creating a booking."""

    user_id: UUID
    customer_id: UUID
    resource_id: int
    start_time: datetime
    end_time: datetime
    description: str | None = None
    booking_type: str | None = None
    location: str | None = None


class BookingService:
    """Service for managing bookings with conflict detection."""

    @provider.inject_session
    async def check_availability(
        self,
        resource_id: int,
        start_time: datetime,
        end_time: datetime,
        session: AsyncSession = None,
    ) -> bool:
        """
        Check if resource is available for the given time range.

        Uses SELECT FOR UPDATE to prevent race conditions during booking creation.
        Returns True if available (no conflicts), False otherwise.
        """
        # Lock rows to prevent concurrent bookings on same resource
        # Cannot use FOR UPDATE with aggregate functions, so select actual rows
        stmt = (
            sa.select(Booking)
            .where(
                sa.and_(
                    Booking.resource_id == resource_id,
                    Booking.start_time < end_time,
                    Booking.end_time > start_time,
                ),
            )
            .with_for_update()
        )
        result = await session.scalars(stmt)
        conflicting_bookings = result.all()
        return len(conflicting_bookings) == 0

    @provider.inject_session
    async def create_booking(
        self,
        params: BookingParams,
        session: AsyncSession = None,
    ) -> Booking | None:
        """
        Create a new booking with availability check and time validation.

        Returns the created Booking or None if validation fails.

        Validations:
        - End time must be after start time
        - Start time must not be in the past
        - End time must not exceed 3 years from now
        """
        now = datetime.now(timezone.utc)

        # Validate time range
        if params.end_time <= params.start_time:
            return None

        # Validate start time is not in the past
        if params.start_time < now:
            return None

        # Validate end time does not exceed 3 years in future
        max_end_time = now + timedelta(days=MAX_BOOKING_DURATION_DAYS)
        if params.end_time > max_end_time:
            return None

        # Check if resource exists and belongs to customer
        resource = await Resource.get(id=params.resource_id, session=session)
        if not resource or resource.customer_id != params.customer_id:
            return None

        # Check availability (includes SELECT FOR UPDATE to prevent race condition)
        is_available = await self.check_availability(
            resource_id=params.resource_id,
            start_time=params.start_time,
            end_time=params.end_time,
            session=session,
        )

        if not is_available:
            return None

        # Create booking
        booking = await Booking.create(
            user_id=params.user_id,
            resource_id=params.resource_id,
            start_time=params.start_time,
            end_time=params.end_time,
            description=params.description,
            booking_type=params.booking_type,
            location=params.location,
            session=session,
        )
        await session.commit()
        return booking

    @provider.inject_session
    async def get_user_bookings(
        self,
        user_id: UUID,
        customer_id: UUID,
        session: AsyncSession = None,
    ) -> list[Booking]:
        """Get all bookings for a user within a customer."""
        stmt = sa.select(Booking).where(
            sa.and_(
                Booking.user_id == user_id,
                # Booking belongs to resources of this customer
                Booking.resource_id.in_(
                    sa.select(Resource.id).where(Resource.customer_id == customer_id),
                ),
            ),
        )
        result = await session.scalars(stmt)
        return result.all()

    @provider.inject_session
    async def get_all_bookings(
        self,
        session: AsyncSession = None,
    ) -> list[Booking]:
        """Get all bookings without filtering by customer."""
        stmt = sa.select(Booking)
        result = await session.scalars(stmt)
        return result.all()

    @provider.inject_session
    async def cancel_booking(
        self,
        booking_id: int,
        user_id: UUID,
        session: AsyncSession = None,
    ) -> bool:
        """
        Cancel (delete) a booking after verifying ownership.

        Security: Rights check is performed BEFORE deletion.
        Returns True if successful, False if booking not found or not owned by user.
        """
        booking = await Booking.get(id=booking_id, session=session)

        # Verify ownership BEFORE any delete operation
        if not booking or booking.user_id != user_id:
            return False

        # Delete using session ORM API to avoid duplication with Base.delete
        await session.delete(booking)
        try:
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        return True
