import asyncio
from datetime import datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import sqlalchemy as sa
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.services.notification.service import NotificationService
from app.infrastructure.database.models.booking import Booking
from app.infrastructure.database.models.notification import (
    Notification,
    NotificationStatus,
)
from app.log import log


class NotificationScheduler:
    def __init__(self, session_factory, notification_service: NotificationService):
        self.session_factory = session_factory
        self.notification_service = notification_service
        self.scheduler = AsyncIOScheduler(
            timezone="UTC",
            job_defaults={
                "coalesce": True,
                "max_instances": 3,
                "misfire_grace_time": 300,
            },
        )
        self.is_running = False
        self.check_interval = 5
        self.batch_size = 50

    async def start(self) -> None:
        """Start the scheduler."""
        if self.is_running:
            return

        trigger = IntervalTrigger(
            minutes=self.check_interval,
            start_date=datetime.now(ZoneInfo("UTC")) + timedelta(seconds=10),
        )

        self.scheduler.add_job(
            self._process_notifications_job,
            trigger=trigger,
            id="process_notifications",
            name="Send notifications",
            replace_existing=True,
        )

        self.scheduler.start()
        self.is_running = True
        log(
            level="info",
            method="start",
            path="NotificationScheduler",
            text_detail="Scheduler started",
        )
        # First run after 5 seconds
        asyncio.create_task(self._process_notifications_job())

    async def stop(self) -> None:
        """Stop the scheduler."""
        if not self.is_running:
            return
        self.scheduler.shutdown(wait=True)

        # Clear cache
        await self.notification_service.clear_bot_cache()

        self.is_running = False
        log(
            level="info",
            method="stop",
            path="NotificationScheduler",
            text_detail="Scheduler stopped",
        )

    async def _process_notifications_job(self):
        """Main task for processing notifications. Gets pending notifications and calls service."""
        try:
            async with self.session_factory() as session:
                notifications = await self._get_pending_notifications(session)
                log(
                    level="info",
                    method="_process_notifications_job",
                    path="NotificationScheduler",
                    text_detail="Starting notification processing task",
                )

                if not notifications:
                    log(
                        level="info",
                        method="_process_notifications_job",
                        path="NotificationScheduler",
                        text_detail="No notifications to send",
                    )
                    return

                log(
                    level="info",
                    method="_process_notifications_job",
                    path="NotificationScheduler",
                    text_detail=f"Found {len(notifications)} notifications to process",
                )

                for notification in notifications:
                    try:
                        # Call service method based on notification type
                        success = await self._send_by_type(notification, session)
                        if not success:
                            log(
                                level="error",
                                method="_process_notifications_job",
                                path="NotificationScheduler",
                                text_detail=f"Failed to send notification {notification.id}",
                            )
                    except Exception as e:  # noqa: BLE001
                        log(
                            level="error",
                            method="_process_notifications_job",
                            path="NotificationScheduler",
                            text_detail=f"Error processing notification {notification.id}: {e}",
                            exception=e,
                        )

                await session.commit()

        except Exception as e:
            log(
                level="error",
                method="_process_notifications_job",
                path="NotificationScheduler",
                text_detail=f"Error in notification processing task: {e}",
                exception=e,
            )

    async def _get_pending_notifications(
        self,
        session: AsyncSession,
    ) -> list[Notification]:
        """Get notifications ready to send."""
        now = datetime.now(ZoneInfo("UTC"))
        stmt = (
            sa.select(Notification)
            .options(
                selectinload(Notification.booking).selectinload(Booking.resource_obj),
                selectinload(Notification.user),
            )
            .where(
                and_(
                    Notification.status == NotificationStatus.PENDING,
                    Notification.scheduled_at <= now,
                    Notification.scheduled_at >= now - timedelta(hours=24),
                ),
            )
            .order_by(Notification.scheduled_at)
            .limit(self.batch_size)
        )

        result = await session.scalars(stmt)
        return result.all()

    async def _send_by_type(
        self,
        notification: Notification,
        session: AsyncSession,
    ) -> bool:
        """Route notification to appropriate service method based on type."""
        notification_type = notification.type

        if notification_type == "booking_24h":
            return await self.notification_service.send_booking_24h(notification)
        if notification_type == "booking_1h":
            return await self.notification_service.send_booking_1h(notification)
        if notification_type == "booking_start":
            return await self.notification_service.send_booking_start(notification)
        if notification_type == "booking_end":
            return await self.notification_service.send_booking_end(notification)
        log(
            level="error",
            method="_send_by_type",
            path="NotificationScheduler",
            text_detail=f"Unknown notification type: {notification_type}",
        )
        return False

    async def force_check(self) -> dict[str, Any]:
        """Force manual check of pending notifications."""
        try:
            await self._process_notifications_job()
            return {"status": "success", "message": "Notification check completed"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
