from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.security import security
from app.depends import AsyncSession, provider
from app.domain.services.bookings import BookingParams, booking_service
from app.infrastructure.database import Booking, Customer, Resource, User

from .schema import BookingCreate, BookingResponse

router = APIRouter(tags=["Bookings"], prefix="/bookings")


@router.post(
    "/",
    response_model=BookingResponse,
    summary="Create a new booking",
    description="Create a booking for a resource at a specific time with conflict "
    "detection",
    responses={
        201: {"description": "Booking created successfully"},
        400: {"description": "Invalid time range or resource not available"},
        403: {"description": "Resource does not belong to your customer"},
        404: {"description": "Resource not found"},
    },
)
async def create_booking(
    data: BookingCreate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """Create a new booking with automatic conflict detection."""
    # Verify customer exists
    customer = await Customer.get(id=data.customer_id, session=session)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer not found",
        )

    # Validate time range
    if data.end_time <= data.start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be after start time",
        )

    # Check if resource exists and belongs to customer
    resource = await Resource.get(id=data.resource_id, session=session)
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found",
        )

    if resource.customer_id != data.customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Resource does not belong to specified customer",
        )

    # Create booking with conflict detection
    booking = await booking_service.create_booking(
        params=BookingParams(
            user_id=current_user.id,
            customer_id=data.customer_id,
            resource_id=data.resource_id,
            start_time=data.start_time,
            end_time=data.end_time,
            source="api",
        ),
        session=session,
    )

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resource is not available for the selected time",
        )

    return BookingResponse(
        **booking.to_dict(),
        resource_name=resource.name,
    )


@router.get(
    "/",
    response_model=list[BookingResponse],
    summary="Get user's bookings",
    description="Get all bookings for the current user within a customer",
    responses={
        200: {"description": "List of bookings"},
        400: {"description": "Missing required customer_id parameter"},
        403: {"description": "Customer not found"},
    },
)
async def list_user_bookings(
    customer_id: UUID,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """Get all bookings for the current user."""
    # Verify customer exists
    customer = await Customer.get(id=customer_id, session=session)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer not found",
        )

    # Get all bookings for user in this customer
    bookings = await booking_service.get_user_bookings(
        user_id=current_user.id,
        customer_id=customer_id,
        session=session,
    )

    # Enrich with resource names
    result = []
    for booking in bookings:
        resource = await Resource.get(id=booking.resource_id, session=session)
        result.append(
            BookingResponse(
                **booking.to_dict(),
                resource_name=resource.name if resource else None,
            ),
        )

    return result


@router.get(
    "/all",
    response_model=list[BookingResponse],
    summary="Get all bookings",
    description="Get all bookings without filtering by customer",
    responses={
        200: {"description": "List of all bookings"},
    },
)
async def list_all_bookings(
    _current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """Get all bookings without customer filter."""
    # Get all bookings
    bookings = await booking_service.get_all_bookings(session=session)

    # Enrich with resource names
    result = []
    for booking in bookings:
        resource = await Resource.get(id=booking.resource_id, session=session)
        result.append(
            BookingResponse(
                **booking.to_dict(),
                resource_name=resource.name if resource else None,
            ),
        )

    return result


@router.delete(
    "/{booking_id}",
    summary="Cancel a booking",
    description="Cancel (delete) a booking by ID",
    responses={
        200: {"description": "Booking cancelled successfully"},
        403: {"description": "Booking does not belong to you"},
        404: {"description": "Booking not found"},
    },
)
async def cancel_booking(
    booking_id: int,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """Cancel (delete) a booking."""
    # Check if booking exists first
    booking = await Booking.get(id=booking_id, session=session)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    # Cancel booking (will check ownership inside service)
    success = await booking_service.cancel_booking(
        booking_id=booking_id,
        user_id=current_user.id,
        source="api",
        session=session,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Booking does not belong to you",
        )

    return {"message": "Booking cancelled successfully"}
