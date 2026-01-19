from typing import Annotated

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
    # Get customer for current user
    customer = await Customer.get_by(owner_id=current_user.id, session=session)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User must be associated with a customer",
        )

    # Validate time range
    if data.end_time <= data.start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be after start time",
        )

    # Check if resource exists
    resource = await Resource.get(id=data.resource_id, session=session)
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found",
        )

    # Check if resource belongs to customer
    if resource.customer_id != customer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Resource does not belong to your customer",
        )

    # Create booking with conflict detection
    booking = await booking_service.create_booking(
        params=BookingParams(
            user_id=current_user.id,
            customer_id=customer.id,
            resource_id=data.resource_id,
            start_time=data.start_time,
            end_time=data.end_time,
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
    description="Get all bookings for the current user within their customer",
    responses={
        200: {"description": "List of bookings"},
        403: {"description": "User must be associated with a customer"},
    },
)
async def list_user_bookings(
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """Get all bookings for the current user."""
    # Get customer for current user
    customer = await Customer.get_by(owner_id=current_user.id, session=session)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User must be associated with a customer",
        )

    # Get all bookings for user in this customer
    bookings = await booking_service.get_user_bookings(
        user_id=current_user.id,
        customer_id=customer.id,
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
        session=session,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Booking does not belong to you",
        )

    return {"message": "Booking cancelled successfully"}
