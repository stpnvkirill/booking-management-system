from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Booking(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    user_id = Column(Integer, nullable=False)
    
    @property
    def is_active(self) -> bool:
        """Проверяет, активно ли бронирование (еще не началось)."""
        return datetime.utcnow() < self.start_time
    
    @property
    def is_current(self) -> bool:
        """Проверяет, идет ли бронирование в данный момент."""
        now = datetime.utcnow()
        return self.start_time <= now < self.end_time
    
    @property
    def is_completed(self) -> bool:
        """Проверяет, завершено ли бронирование."""
        return datetime.utcnow() >= self.end_time
    
    @property
    def is_24h_notification_due(self) -> bool:
        """Проверяет, нужно ли отправить уведомление за 24 часа до начала."""
        if not self.is_active:
            return False
        
        now = datetime.utcnow()
        notification_time = self.start_time - timedelta(hours=24)
        return now >= notification_time
    
    @property
    def is_1h_notification_due(self) -> bool:
        """Проверяет, нужно ли отправить уведомление за 1 час до начала."""
        if not self.is_active:
            return False
        
        now = datetime.utcnow()
        notification_time = self.start_time - timedelta(hours=1)
        return now >= notification_time
    
    @property
    def duration(self) -> timedelta:
        """Возвращает длительность бронирования."""
        return self.end_time - self.start_time
    
    @property
    def time_until_start(self) -> Optional[timedelta]:
        """Возвращает время до начала бронирования."""
        now = datetime.utcnow()
        if self.is_active:
            return self.start_time - now
        return None
    
    @property
    def time_remaining(self) -> Optional[timedelta]:
        """Возвращает оставшееся время бронирования."""
        now = datetime.utcnow()
        if self.is_current:
            return self.end_time - now
        return None
