from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

import sqlalchemy as sa

from app.depends import AsyncSession, provider
from app.infrastructure.database import Booking, Resource


@dataclass
class BookingParams:
    """Parameters for creating a booking."""

    user_id: UUID
    customer_id: UUID
    resource_id: int
    start_time: datetime
    end_time: datetime


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

        Returns True if available (no conflicts), False otherwise.
        """
        stmt = sa.select(sa.func.count(Booking.id)).where(
            sa.and_(
                Booking.resource_id == resource_id,
                Booking.start_time < end_time,
                Booking.end_time > start_time,
            ),
        )
        count = await session.scalar(stmt)
        return count == 0

    @provider.inject_session
    async def create_booking(
        self,
        params: BookingParams,
        session: AsyncSession = None,
    ) -> Booking | None:
        """
        Create a new booking with availability check.

        Returns the created Booking or None if not available.
        """
        # Check if end_time > start_time
        if params.end_time <= params.start_time:
            return None

        # Check if resource exists and belongs to customer
        resource = await Resource.get(id=params.resource_id, session=session)
        if not resource or resource.customer_id != params.customer_id:
            return None

        # Check availability
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
    async def cancel_booking(
        self,
        booking_id: int,
        user_id: UUID,
        session: AsyncSession = None,
    ) -> bool:
        """
        Cancel (delete) a booking.

        Returns True if successful, False if booking not found or not owned by user.
        """
        booking = await Booking.get(id=booking_id, session=session)

        if not booking or booking.user_id != user_id:
            return False

        # perform delete using the provided AsyncSession to avoid relying on
        # Base.delete implementation which may assume different session helpers
        stmt = sa.delete(Booking).where(Booking.id == booking_id)
        await session.execute(stmt)
        try:
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        return True

    @provider.inject_session
    async def get_booking_with_resource(
        self,
        booking_id: int,
        session: AsyncSession = None,
    ) -> tuple[Booking, Resource] | None:
        """Get booking with its resource details (for response formatting)."""
        booking = await Booking.get(id=booking_id, session=session)
        if not booking:
            return None

        resource = await Resource.get(id=booking.resource_id, session=session)
        return (booking, resource) if resource else None
