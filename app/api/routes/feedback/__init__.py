from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
import sqlalchemy as sa

from app.api.security import security
from app.depends import AsyncSession, provider
from app.infrastructure.database import Booking, Feedback, User

from .schema import FeedbackCreate, FeedbackResponse

router = APIRouter(
    tags=["Feedback"],
    prefix="/feedback",
)


@router.post(
    "/",
    response_model=FeedbackResponse,
    summary="Create feedback for a booking",
    description="Create a feedback (rating and comment) for a completed booking",
    responses={
        201: {"description": "Feedback created successfully"},
        400: {"description": "Feedback already exists or booking not completed"},
        403: {"description": "Booking does not belong to the user"},
        404: {"description": "Booking not found"},
    },
)
async def create_feedback(
    data: FeedbackCreate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """Create feedback for a completed booking."""

    # 1️⃣ Проверяем, что бронирование существует
    booking = await Booking.get(id=data.booking_id, session=session)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    # 2️⃣ Проверяем, что бронирование принадлежит пользователю
    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Booking does not belong to the current user",
        )

    # 3️⃣ Проверяем, что бронирование завершено
    if booking.end_time > sa.func.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot leave feedback for an active booking",
        )

    # 4️⃣ Проверяем, что отзыв ещё не был оставлен
    stmt = sa.select(Feedback).where(
        Feedback.booking_id == data.booking_id,
    )
    existing_feedback = await session.scalar(stmt)

    if existing_feedback:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Feedback for this booking already exists",
        )

    # 5️⃣ Создаём отзыв
    feedback = Feedback(
        booking_id=data.booking_id,
        user_id=current_user.id,
        customer_id=booking.customer_id,
        rating=data.rating,
        comment=data.comment,
    )

    session.add(feedback)
    await session.commit()
    await session.refresh(feedback)

    return feedback
