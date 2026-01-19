from datetime import datetime, timedelta
from typing import Optional

from config import config
from sqlalchemy import Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from app.infrastructure.database.models.booking import Booking

# Создаем базовый класс для моделей
Base = declarative_base()



class Booking(Base):
    """
    Модель бронирования.
    Хранит информацию о бронировании и статусах отправки уведомлений.
    """


    def is_24h_notification_due(self, booking: Booking) -> bool:
        """Проверяет, нужно ли отправить уведомление за 24 часа до начала."""
        if not self.is_active():
            return False
        
        now = datetime.utcnow()
        notification_time = booking.start_time - timedelta(hours=24)
        return now >= notification_time and booking.start_time > now

    def is_1h_notification_due(self, booking: Booking) -> bool:
        """Проверяет, нужно ли отправить уведомление за 1 час до начала."""
        if not self.is_active():
            return False
        
        now = datetime.utcnow()
        notification_time = booking.start_time - timedelta(hours=1)
        return now >= notification_time and booking.start_time > now

   

    def is_active(self) -> bool:
        """Проверяет, активно ли бронирование (еще не началось)."""
        now = datetime.utcnow()
        return now < self.start_time

    def is_current(self, booking: Booking) -> bool:
        """Проверяет, идет ли бронирование в данный момент."""
        now = datetime.utcnow()
        return booking.start_time <= now < booking.end_time

    def is_completed(self, booking: Booking) -> bool:
        """Проверяет, завершено ли бронирование."""
        return datetime.utcnow() >= booking.end_time

    def is_upcoming(self, booking: Booking) -> bool:
        """Проверяет, является ли бронирование предстоящим."""
        now = datetime.utcnow()
        return now < booking.start_time

    def duration(self, booking: Booking) -> timedelta:
        """Возвращает длительность бронирования."""
        return booking.end_time - booking.start_time

    def time_until_start(self, booking: Booking) -> Optional[timedelta]:
        """Возвращает время до начала бронирования, если оно еще не началось."""
        now = datetime.utcnow()
        if now < booking.start_time:
            return booking.start_time - now
        return None

    def time_remaining(self, booking: Booking) -> Optional[timedelta]:
        """Возвращает оставшееся время бронирования, если оно активно."""
        now = datetime.utcnow()
        if self.is_current():
            return booking.end_time - now
        return None


