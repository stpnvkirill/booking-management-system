from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime


class Booking:
    """
    Модель бронирования с методами для проверки необходимости уведомлений
    24-часового и 1-часового напоминаний.
    """

    # Время создания записи
    created_at = Column(DateTime, default=datetime.utcnow)

    otified_24h = Column(Boolean, default=False)  # Уведомление за 24 часа
    notified_1h = Column(Boolean, default=False)  # Уведомление за 1 час

    def is_24h_notification_due(self) -> bool:
        if self.notified_24h:
            return False
        # now = datetime.utcnow()

    def is_1h_notification_due(self) -> bool:
        if self.notified_1h:
            return False
        # now = datetime.utcnow()

    def is_active(self) -> bool:
        return datetime.utcnow() < self.booking_time


def get_db():
    pass
