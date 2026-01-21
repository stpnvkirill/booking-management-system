from dataclasses import dataclass  # noqa: INP001


@dataclass
class ReminderResult:
    """Результат отправки напоминания"""

    booking_id: int
    user_id: int
    success: bool
    error_message: str | None = None


class NotificationManager:
    """Менеджер для управления состоянием уведомлений"""

    _sent_notifications = set()  # поменять  # noqa: RUF012

    @classmethod
    def is_notification_sent(cls, booking_id: int, reminder_type: str) -> bool:
        key = f"{booking_id}_{reminder_type}"
        return key in cls._sent_notifications

    @classmethod
    def mark_notification_sent(cls, booking_id: int, reminder_type: str):
        key = f"{booking_id}_{reminder_type}"
        cls._sent_notifications.add(key)
