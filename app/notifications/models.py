from datetime import datetime, timedelta

from config import config
from sqlalchemy import Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from app.infrastructure.database import Booking as book
# Создаем базовый класс для моделей
Base = declarative_base()

class Booking_cl(Base):
    """
    Модель бронирования.
    Хранит информацию о бронировании и статусах отправки уведомлений.
    """
    notified_24h = book.start_time < book.end_time  # Уведомление за 24 часа до начала
    notified_1h = book.end_time - datetime.datetime.now()   # Уведомление за 1 час до начала
    def is_24h_notification_due(self) -> bool:
        """Проверяет, нужно ли отправить уведомление за 24 часа до начала."""
        if self.notified_24h:
            return False
        now = datetime.utcnow()
        notification_time = book.start_time - timedelta(hours=24)
        return now >= notification_time

    def is_1h_notification_due(self) -> bool:
        """Проверяет, нужно ли отправить уведомление за 1 час до начала."""
        if self.notified_1h:
            return False
        now = datetime.utcnow()
        notification_time = book.start_time - timedelta(hours=1)
        return now >= notification_time

    def is_active(self) -> bool:
        """Проверяет, активно ли бронирование (еще не началось)."""
        return datetime.utcnow() < book.start_time

    def is_current(self) -> bool:
        """Проверяет, идет ли бронирование в данный момент."""
        now = datetime.utcnow()
        return book.start_time <= now < book.end_time

    def is_completed(self) -> bool:
        """Проверяет, завершено ли бронирование."""
        return datetime.utcnow() >= book.end_time


