from datetime import datetime, timedelta

from config import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем базовый класс для моделей
Base = declarative_base()

# Создаем подключение к базе данных
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Booking(Base):
    """
    Модель бронирования.
    Хранит информацию о бронировании и статусах отправки уведомлений.
    """

    def is_24h_notification_due(self) -> bool:
        """Проверяет, нужно ли отправить уведомление за 24 часа до начала."""
        if self.notified_24h:
            return False
        now = datetime.utcnow()
        notification_time = self.start_time - timedelta(hours=24)
        return now >= notification_time

    def is_1h_notification_due(self) -> bool:
        """Проверяет, нужно ли отправить уведомление за 1 час до начала."""
        if self.notified_1h:
            return False
        now = datetime.utcnow()
        notification_time = self.start_time - timedelta(hours=1)
        return now >= notification_time

    def is_active(self) -> bool:
        """Проверяет, активно ли бронирование (еще не началось)."""
        return datetime.utcnow() < self.start_time

    def is_current(self) -> bool:
        """Проверяет, идет ли бронирование в данный момент."""
        now = datetime.utcnow()
        return self.start_time <= now < self.end_time

    def is_completed(self) -> bool:
        """Проверяет, завершено ли бронирование."""
        return datetime.utcnow() >= self.end_time


# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)


