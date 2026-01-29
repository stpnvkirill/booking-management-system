import contextlib
from datetime import datetime, timedelta, timezone

import sqlalchemy as sa
from sqlalchemy import and_

from app.depends import AsyncSession, provider
from app.infrastructure.database import Booking
from app.infrastructure.database.models.feedback import Feedback
from app.infrastructure.database.models.notification import (
    Notification,
    NotificationStatus,
    NotificationType,
)
from app.log import log


class EvaluationNotificationService:
    """Service that creates evaluation request notifications for completed bookings."""

    @provider.inject_session
    async def create_evaluation_notifications(
        self,
        *,
        session: AsyncSession | None = None,
    ) -> None:
        """Creates evaluation notifications for completed bookings."""
        try:
            now = datetime.now(timezone.utc)
            # Find bookings that ended between 15 minutes ago and 24 hours ago
            # This ensures we catch bookings that are ready for evaluation requests
            min_end_time = now - timedelta(hours=24)
            max_end_time = now - timedelta(minutes=15)

            stmt = (
                sa.select(Booking)
                .where(
                    and_(
                        Booking.end_time >= min_end_time,
                        Booking.end_time <= max_end_time,
                    ),
                )
                .order_by(Booking.end_time.desc())
            )

            result = await session.scalars(stmt)
            completed_bookings = result.all()

            if not completed_bookings:
                log(
                    level="info",
                    method="create_evaluation_notifications",
                    path="FeedbackModule",
                    text_detail="There are no completed bookings to create evaluation requests",  # noqa: E501
                )
                return

            log(
                level="info",
                method="create_evaluation_notifications",
                path="FeedbackModule",
                text_detail=f"Checking {len(completed_bookings)} completed bookings to create evaluation requests",  # noqa: E501
            )

            created_count = 0
            for booking in completed_bookings:
                try:
                    if await self.create_notification_if_needed(booking, session):
                        created_count += 1
                except Exception as e:  # noqa: BLE001
                    log(
                        level="error",
                        method="create_evaluation_notifications",
                        path="FeedbackModule",
                        text_detail=f"Error when creating an assessment request for a booking {booking.id}: {e}",  # noqa: E501
                    )
                    # Rollback on error to allow session to continue
                    with contextlib.suppress(Exception):
                        await session.rollback()

            if created_count > 0:
                await session.commit()
                log(
                    level="info",
                    method="create_evaluation_notifications",
                    path="FeedbackModule",
                    text_detail=f"{created_count} rating requests have been created",
                )
            else:
                # Commit even if no notifications were created to clear any pending stat
                await session.commit()

        except Exception as e:  # noqa: BLE001
            log(
                level="error",
                method="create_evaluation_notifications",
                path="FeedbackModule",
                text_detail=f"Error in the evaluation request creation service: {e}",
            )
            # Rollback on error
            with contextlib.suppress(Exception):
                await session.rollback()

    async def create_notification_if_needed(
        self,
        booking: Booking,
        session: AsyncSession,
    ) -> bool:
        """Creates evaluation notification if needed. Returns True if created."""
        # Check if feedback already exists for this booking/user
        feedback_stmt = sa.select(Feedback).where(
            and_(
                Feedback.booking_id == booking.id,
                Feedback.user_id == booking.user_id,
            ),
        )
        existing_feedback = await session.scalar(feedback_stmt)

        if existing_feedback:
            log(
                level="info",
                method="create_notification_if_needed",
                path="FeedbackModule",
                text_detail=f"The review already exists for booking {booking.id}",
            )
            return False

        # Check if evaluation notification already exists
        notification_stmt = sa.select(Notification).where(
            and_(
                Notification.booking_id == booking.id,
                Notification.type == NotificationType.BOOKING_EVALUATION_REQUEST,
            ),
        )
        existing_notification = await session.scalar(notification_stmt)

        if existing_notification:
            log(
                level="info",
                method="create_notification_if_needed",
                path="FeedbackModule",
                text_detail=f"An evaluation request has already been created for booking {booking.id}",  # noqa: E501
            )
            return False

        # Create evaluation notification scheduled for 15 minutes after booking completion  # noqa: E501
        evaluation_scheduled_at = booking.end_time + timedelta(minutes=15)

        # If the scheduled time has already passed, set it to now so it gets sent immediately  # noqa: E501
        now = datetime.now(timezone.utc)
        evaluation_scheduled_at = max(now, evaluation_scheduled_at)

        notification = Notification(
            booking_id=booking.id,
            user_id=booking.user_id,
            type=NotificationType.BOOKING_EVALUATION_REQUEST,
            status=NotificationStatus.PENDING,
            scheduled_at=evaluation_scheduled_at,
        )
        session.add(notification)
        await session.flush()

        log(
            level="info",
            method="create_notification_if_needed",
            path="FeedbackModule",
            text_detail=f"An evaluation request has been created for booking {booking.id}, scheduled for {evaluation_scheduled_at}",  # noqa: E501
        )
        return True
