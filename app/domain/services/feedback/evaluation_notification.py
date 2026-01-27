"""Service for creating evaluation request notifications for completed bookings."""

import asyncio
import contextlib
from datetime import datetime, timedelta, timezone
import logging

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

logger = logging.getLogger(__name__)


class EvaluationNotificationService:
    """Service that creates evaluation request notifications for completed bookings."""

    def __init__(self, poll_interval_seconds: int = 300):  # 5 minutes
        self.poll_interval_seconds = poll_interval_seconds
        self._service_task: asyncio.Task | None = None

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
                logger.debug(
                    "Нет завершенных бронирований для создания запросов на оценку"
                )
                return

            logger.info(
                f"Проверка {len(completed_bookings)} завершенных бронирований для создания запросов на оценку",  # noqa: E501, G004
            )

            created_count = 0
            for booking in completed_bookings:
                try:
                    if await self.create_notification_if_needed(booking, session):
                        created_count += 1
                except Exception as e:  # noqa: BLE001
                    logger.error(
                        f"Ошибка при создании запроса на оценку для бронирования {booking.id}: {e}",  # noqa: E501, G004
                    )
                    # Rollback on error to allow session to continue
                    with contextlib.suppress(Exception):
                        await session.rollback()

            if created_count > 0:
                await session.commit()
                logger.info(f"Создано {created_count} запросов на оценку")  # noqa: G004
            else:
                # Commit even if no notifications were created to clear any pending state
                await session.commit()

        except Exception as e:
            logger.error(
                f"Ошибка в сервисе создания запросов на оценку: {e}",  # noqa: G004
                exc_info=True,
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
            logger.debug(
                f"Отзыв уже существует для бронирования {booking.id}, пропускаем",  # noqa: G004
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
            logger.debug(
                f"Запрос на оценку уже создан для бронирования {booking.id}, пропускаем",  # noqa: G004
            )
            return False

        # Create evaluation notification scheduled for 15 minutes after booking completion
        evaluation_scheduled_at = booking.end_time + timedelta(minutes=15)

        # If the scheduled time has already passed, set it to now so it gets sent immediately
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

        logger.info(
            f"Создан запрос на оценку для бронирования {booking.id}, "  # noqa: G004
            f"запланирован на {evaluation_scheduled_at}",
        )
        return True

    async def service_loop(self) -> None:
        """Background loop that periodically creates evaluation notifications."""
        try:
            while True:
                await self.create_evaluation_notifications()
                await asyncio.sleep(self.poll_interval_seconds)
        except asyncio.CancelledError:
            raise
        except Exception as e:
            logger.error(
                f"Критическая ошибка в сервисе создания запросов на оценку: {e}",
                exc_info=True,
            )  # noqa: E501, G004

    async def start(self) -> None:
        """Start the evaluation notification service."""
        if self._service_task is not None and not self._service_task.done():
            return
        self._service_task = asyncio.create_task(self.service_loop())
        logger.info("Сервис создания запросов на оценку запущен")

    async def stop(self) -> None:
        """Stop the evaluation notification service."""
        if self._service_task is None:
            return
        if not self._service_task.done():
            self._service_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._service_task
        self._service_task = None
        logger.info("Сервис создания запросов на оценку остановлен")


# Global instance
feedback_service = EvaluationNotificationService()
