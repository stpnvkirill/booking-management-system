from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from app.infrastructure.database.models.booking import Booking


class NotificationMessageFactory(ABC):
    """Abstract factory for creating notification messages."""

    @abstractmethod
    def create_message(self, booking: "Booking") -> str:
        pass


class Booking24HMessageFactory(NotificationMessageFactory):
    """Message 24 hours before booking."""

    def create_message(self, booking: "Booking") -> str:
        (booking.end_time - booking.start_time).total_seconds() / 3600
        return (
            "Booking reminder!\n\n"
            "Your booking starts in 24 hours:\n"
            f"Date: {booking.start_time.strftime('%d.%m.%Y')}\n"
            f"Time: {booking.start_time.strftime('%H:%M')}\n"
            f"Location: [specify location]"
        )


class Booking1HMessageFactory(NotificationMessageFactory):
    """Message 1 hour before booking."""

    def create_message(self, booking: "Booking") -> str:
        duration_hours = (booking.end_time - booking.start_time).total_seconds() / 3600
        return (
            "Booking starts soon!\n\n"
            "Starts in 1 hour:\n"
            f"{booking.start_time.strftime('%d.%m.%Y %H:%M')}\n"
            f"Duration: {duration_hours:.1f} hours"
        )


class BookingStartMessageFactory(NotificationMessageFactory):
    """Message about booking start."""

    def create_message(self, booking: "Booking") -> str:
        return (
            "Booking started!\n\n"
            "Your time is booked until:\n"
            f"{booking.end_time.strftime('%H:%M')}"
        )


class BookingEndMessageFactory(NotificationMessageFactory):
    """Message about booking end."""

    def create_message(self, booking: "Booking") -> str:
        return (
            "Booking ends soon!\n\n"
            "Ends in 5 minutes.\n"
            f"End time: {booking.end_time.strftime('%H:%M')}"
        )


class BookingEvaluationRequestMessageFactory(NotificationMessageFactory):
    """Message requesting evaluation after booking completion."""

    def create_message(self, booking: "Booking") -> str:
        return (
            "Оцените ваше бронирование!\n\n"
            f"Бронирование завершено: {booking.end_time.strftime('%d.%m.%Y %H:%M')}\n\n"
            "Пожалуйста, оцените ваше бронирование от 1 до 5 звезд.\n"
            "Вы также можете оставить комментарий.\n\n"
            "Используйте команду /feedback для оценки."
        )


class NotificationFactory:
    """Factory for creating messages by notification type."""

    _factories: ClassVar[dict[str, NotificationMessageFactory]] = {
        "booking_24h": Booking24HMessageFactory(),
        "booking_1h": Booking1HMessageFactory(),
        "booking_start": BookingStartMessageFactory(),
        "booking_end": BookingEndMessageFactory(),
        "booking_eval": BookingEvaluationRequestMessageFactory(),
    }

    @classmethod
    def create_message(cls, notification_type, booking: "Booking") -> str:
        """Create message for specified notification type."""
        # If it's enum, convert to string
        type_str = (
            notification_type.value
            if hasattr(notification_type, "value")
            else str(notification_type)
        )

        factory = cls._factories.get(type_str)
        if not factory:
            msg = f"Unknown notification type: {type_str}"
            raise ValueError(msg)

        return factory.create_message(booking)
